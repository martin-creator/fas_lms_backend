from django.contrib import admin
from .models import Certification, Attachment
from activity.models import Category
from django.contrib.contenttypes.admin import GenericTabularInline

# Inline for GenericRelation Attachment
class AttachmentInline(GenericTabularInline):
    model = Attachment
    extra = 1


@admin.action(description='Revoke selected certifications')
def revoke_certifications(modeladmin, request, queryset):
    for cert in queryset:
        cert.revoke(reason="Revoked by admin")
        # Send notification
        from services.utils.notification import send_notification
        send_notification(cert.user, f"Your certification '{cert.name}' has been revoked.")

# ModelAdmin for Certification
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'issue_date', 'expiration_date', 'verification_status')
    list_filter = ('issue_date', 'expiration_date', 'verification_status', 'categories')
    search_fields = ('name', 'user__username', 'issuing_organization', 'description')
    actions = [revoke_certifications]


    fieldsets = (
        ('Certification Information', {
            'fields': ('name', 'user', 'issuing_organization', 'issue_date', 'expiration_date', 'verification_status')
        }),
        ('Additional Details', {
            'fields': ('credential_id', 'credential_url', 'description', 'certificate_image', 'categories', 'related_jobs', 'related_courses')
        }),
    )

    filter_horizontal = ('categories', 'related_jobs', 'related_courses')
    inlines = [AttachmentInline]

    def save_model(self, request, obj, form, change):
        """Override save_model to associate the user with the Certification."""
        if not obj.user_id:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        """Limit queryset to current user's Certifications."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def get_readonly_fields(self, request, obj=None):
        """Limit fields that are readonly based on user permissions."""
        if request.user.is_superuser:
            return []
        return ['user', 'verification_status']

    def get_inline_instances(self, request, obj=None):
        """Override to hide AttachmentInline for non-superusers."""
        if request.user.is_superuser:
            return super().get_inline_instances(request, obj)
        return []


