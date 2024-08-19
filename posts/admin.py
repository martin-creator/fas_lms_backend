from django.contrib import admin
from django import forms
from taggit.forms import TagWidget
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment
from activity.models import Attachment, Reaction
from django.utils.html import format_html, format_html_join


# Inline for GenericRelation Attachment
class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 1

# Inline for replies (child comments)
class ReplyInline(admin.TabularInline):  # or admin.StackedInline if you prefer
    model = Comment
    fk_name = 'parent_comment'
    fields = ('author', 'content', 'visibility', 'created_at')  # Adjust fields as necessary
    readonly_fields = ('created_at',)
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        # Override get_formset to set the parent comment dynamically
        formset = super().get_formset(request, obj, **kwargs)
        formset.parent_obj = obj  # Store the parent comment object in the formset
        return formset

    def get_queryset(self, request):
        # Override get_queryset to filter only direct replies to the current comment
        queryset = super().get_queryset(request)
        parent_obj = getattr(self.formset, 'parent_obj', None)
        if parent_obj:
            return queryset.filter(parent_comment=parent_obj)
        else:
            return queryset.none()

# Custom Admin Form for Post
class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'tags': TagWidget,
        }

# class ReactionInline(admin.TabularInline):
#     model = Reaction
#     extra = 0
#     readonly_fields = ('user', 'type', 'created_at')
#     can_delete = False

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         # Filter the queryset if necessary
#         return queryset.filter(content_type=ContentType.objects.get_for_model(Post))

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('id', 'author', 'content_preview', 'group', 'visibility', 'created_at', 'total_reactions')
    list_filter = ('visibility', 'created_at', 'author')
    search_fields = ('content', 'author__username', 'group__name')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'display_reactions')
    fieldsets = (
        (None, {
            'fields': ('author', 'group', 'content', 'visibility', 'categories')
        }),
        ('Reactions', {
            'fields': ('display_reactions',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    # No need for ReactionInline

    def total_reactions(self, obj):
        # Count reactions directly from the GenericRelation
        return format_html('<strong>{}</strong>', obj.reactions.count())

    total_reactions.short_description = 'Total Reactions'

    def display_reactions(self, obj):
        reactions = obj.reactions.all()
        if reactions.exists():
            return format_html(
                '<ul>{}</ul>',
                format_html_join(
                    '',
                    '<li><strong>{}</strong>: {}</li>',
                    ((reaction.user.username, reaction.type) for reaction in reactions)
                )
            )
        return "No reactions yet"

    display_reactions.short_description = "Reactions"

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content


    


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'content_preview', 'visibility', 'created_at', 'total_reactions')
    list_filter = ('visibility', 'created_at', 'author')
    search_fields = ('content', 'author__username', 'post__content')
    date_hierarchy = 'created_at'
    filter_horizontal = ()
    readonly_fields = ('created_at', 'updated_at', 'display_reactions')
    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'content', 'visibility')
        }),
        ('Reactions', {
            'fields': ('display_reactions',),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    inlines = [AttachmentInline, ReplyInline]  # Include ReplyInline here

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'

    def total_reactions(self, obj):
        # Count reactions directly from the GenericRelation
        return format_html('<strong>{}</strong>', obj.reactions.count())

    total_reactions.short_description = 'Total Reactions'

    def display_reactions(self, obj):
        reactions = obj.reactions.all()
        if reactions.exists():
            return format_html(
                '<ul>{}</ul>',
                format_html_join(
                    '',
                    '<li><strong>{}</strong>: {}</li>',
                    ((reaction.user.username, reaction.type) for reaction in reactions)
                )
            )
        return "No reactions yet"
    display_reactions.short_description = "Reactions"
