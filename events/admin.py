from django.contrib import admin
from .models import Event, EventRegistration, EventFeedback
from profiles.models import UserProfile
from activity.models import Attachment, Category
from django.contrib.contenttypes.admin import GenericTabularInline

# Inline for GenericRelation Attachment
class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'location', 'start_time', 'end_time', 'get_attendees_count')
    list_filter = ('organizer', 'location', 'start_time', 'end_time',)
    search_fields = ('title', 'organizer__user__username', 'location')

    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'description', 'organizer', 'categories', 'location', 'start_time', 'end_time', 'capacity', 'category')
        }),
    )

    filter_horizontal = ('categories', 'attendees')
    inlines = [AttachmentInline]

    readonly_fields = ('get_attendees_count',)  # Assuming this is a readonly method

    def get_attendees_count(self, obj):
        """Custom method to display number of attendees."""
        return obj.attendees.count()
    get_attendees_count.short_description = 'Attendees'

    def save_model(self, request, obj, form, change):
        """Override save_model to associate the current user with the Event."""
        if not obj.pk:  # Only set organizer on creation
            obj.organizer = UserProfile.objects.get(user=request.user)
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        """Override get_form to exclude attachments field."""
        form = super().get_form(request, obj, **kwargs)
        if 'attachments' in form.base_fields:
            del form.base_fields['attachments']
        return form

    def get_inline_instances(self, request, obj=None):
        """Override get_inline_instances to pass request to inlines."""
        inline_instances = []
        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            if request:
                inline.request = request
            inline_instances.append(inline)
        return inline_instances


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendee', 'registration_date')
    list_filter = ('event', 'attendee', 'registration_date')
    search_fields = ('event__title', 'attendee__user__username')

    def save_model(self, request, obj, form, change):
        """Override save_model to associate the current user with the EventRegistration."""
        if not obj.pk:
            obj.attendee = UserProfile.objects.get(user=request.user)

        obj.save()

    
@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendee', 'rating', 'feedback', 'feedback_date')
    list_filter = ('event', 'attendee', 'rating', 'feedback_date')
    search_fields = ('event__title', 'attendee__user__username')

    def save_model(self, request, obj, form, change):
        """Override save_model to associate the current user with the EventFeedback."""
        if not obj.pk:
            obj.attendee = UserProfile.objects.get(user=request.user)

        obj.save()