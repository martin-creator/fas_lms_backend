from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import (
    NotificationType,
    Notification,
    NotificationTemplate,
    NotificationSettings,
    NotificationReadStatus,
    UserNotificationPreference,
    NotificationSnooze,
    NotificationEngagement,
    NotificationABTest,
    NotificationLog
)

class NotificationTypeForm(forms.ModelForm):
    predefined_types = forms.ChoiceField(
        choices=[(type_name, type_name) for type_name in NotificationType.PREDEFINED_TYPES],
        required=False,
        label='Predefined Types'
    )
    custom_type = forms.CharField(
        max_length=100,
        required=False,
        label='Custom Type'
    )

    class Meta:
        model = NotificationType
        fields = ['predefined_types', 'custom_type']

    def clean(self):
        cleaned_data = super().clean()
        predefined_type = cleaned_data.get('predefined_types')
        custom_type = cleaned_data.get('custom_type')

        if not predefined_type and not custom_type:
            raise forms.ValidationError(_('You must select a predefined type or enter a custom type.'))

        if predefined_type and custom_type:
            raise forms.ValidationError(_('You can only select one type: either a predefined type or a custom type.'))

        return cleaned_data

    def save(self, commit=True):
        predefined_type = self.cleaned_data.get('predefined_types')
        custom_type = self.cleaned_data.get('custom_type')

        if predefined_type:
            self.instance.type_name = predefined_type
        elif custom_type:
            self.instance.type_name = custom_type

        return super().save(commit=commit)


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        # Exclude non-editable fields and handle GenericForeignKey
        exclude = ['timestamp', 'created_at', 'updated_at', 'content_object']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError(_('Content cannot be empty.'))
        return content

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url and not url.startswith(('http', 'https')):
            raise forms.ValidationError(_('URL must start with http or https.'))
        return url


class NotificationTemplateForm(forms.ModelForm):
    class Meta:
        model = NotificationTemplate
        fields = ['notification_type', 'template']

    def clean_template(self):
        template = self.cleaned_data.get('template')
        if not template:
            raise forms.ValidationError(_('Template content cannot be empty.'))
        return template


class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = NotificationSettings
        fields = ['user', 'notification_type', 'is_enabled', 'channel_preferences']

    def clean_channel_preferences(self):
        preferences = self.cleaned_data.get('channel_preferences')
        if not isinstance(preferences, dict):
            raise forms.ValidationError(_('Channel preferences must be a JSON object.'))
        return preferences


class NotificationReadStatusForm(forms.ModelForm):
    class Meta:
        model = NotificationReadStatus
        fields = ['user', 'notification', 'is_read', 'read_at']

    def clean_read_at(self):
        read_at = self.cleaned_data.get('read_at')
        if read_at and read_at > timezone.now():
            raise forms.ValidationError(_('Read at time cannot be in the future.'))
        return read_at


class UserNotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserNotificationPreference
        fields = ['user', 'email_notifications', 'sms_notifications', 'push_notifications', 'notification_frequency']

    def clean_notification_frequency(self):
        frequency = self.cleaned_data.get('notification_frequency')
        if frequency not in dict(UserNotificationPreference.NOTIFICATION_FREQUENCY):
            raise forms.ValidationError(_('Invalid notification frequency.'))
        return frequency


class NotificationSnoozeForm(forms.ModelForm):
    class Meta:
        model = NotificationSnooze
        fields = ['user', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and end_time <= start_time:
            raise ValidationError(_('End time must be after start time.'))

        return cleaned_data


class NotificationEngagementForm(forms.ModelForm):
    class Meta:
        model = NotificationEngagement
        fields = ['notification', 'user', 'clicked_at', 'interaction_type']

    def clean_clicked_at(self):
        clicked_at = self.cleaned_data.get('clicked_at')
        viewed_at = self.instance.viewed_at

        if clicked_at and viewed_at and clicked_at < viewed_at:
            raise ValidationError(_('Clicked at time cannot be before viewed at time.'))

        return clicked_at


class NotificationABTestForm(forms.ModelForm):
    class Meta:
        model = NotificationABTest
        fields = ['test_name', 'variant', 'notification_template', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise ValidationError(_('End date must be after start date.'))

        return cleaned_data


class NotificationLogForm(forms.ModelForm):
    class Meta:
        model = NotificationLog
        fields = ['notification', 'action', 'performed_by']  # Removed 'timestamp'

    def clean(self):
        cleaned_data = super().clean()
        # Add any custom validation here if needed

        return cleaned_data