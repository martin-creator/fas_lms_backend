# Generated by Django 5.0.6 on 2024-07-24 16:11

import django.db.models.deletion
import notifications.utils.delivery_method
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0007_alter_notification_object_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={
                "permissions": [
                    ("can_manage_notifications", "Can manage notifications"),
                    ("can_view_notifications", "Can view notifications"),
                ]
            },
        ),
        migrations.AddField(
            model_name="notification",
            name="delivery_method",
            field=models.CharField(
                choices=[
                    (
                        notifications.utils.delivery_method.DeliveryMethod["EMAIL"],
                        "EMAIL",
                    ),
                    (notifications.utils.delivery_method.DeliveryMethod["SMS"], "SMS"),
                    (
                        notifications.utils.delivery_method.DeliveryMethod["PUSH"],
                        "PUSH",
                    ),
                    (
                        notifications.utils.delivery_method.DeliveryMethod["IN_APP"],
                        "IN_APP",
                    ),
                ],
                default="IN_APP",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="html_content",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="notification",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("es", "Spanish"), ("fr", "French")],
                default="en",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="notification",
            name="metadata",
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name="notification",
            name="read_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="notification",
            name="severity",
            field=models.CharField(
                choices=[("info", "Info"), ("warning", "Warning"), ("alert", "Alert")],
                default="info",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="content",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name="notificationsettings",
            unique_together={("user", "notification_type")},
        ),
        migrations.CreateModel(
            name="NotificationABTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("test_name", models.CharField(max_length=100)),
                ("variant", models.CharField(max_length=50)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                (
                    "notification_template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="notifications.notificationtemplate",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NotificationEngagement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("viewed_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("clicked_at", models.DateTimeField(blank=True, null=True)),
                (
                    "interaction_type",
                    models.CharField(
                        choices=[
                            ("view", "View"),
                            ("click", "Click"),
                            ("dismiss", "Dismiss"),
                        ],
                        default="view",
                        max_length=20,
                    ),
                ),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="notifications.notification",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NotificationLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("action", models.CharField(max_length=50)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="notifications.notification",
                    ),
                ),
                (
                    "performed_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NotificationSnooze",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserNotificationPreference",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email_notifications", models.BooleanField(default=True)),
                ("sms_notifications", models.BooleanField(default=True)),
                ("push_notifications", models.BooleanField(default=True)),
                (
                    "notification_frequency",
                    models.CharField(
                        choices=[
                            ("IMMEDIATE", "Immediate"),
                            ("HOURLY_DIGEST", "Hourly Digest"),
                            ("DAILY_DIGEST", "Daily Digest"),
                            ("WEEKLY_DIGEST", "Weekly Digest"),
                        ],
                        default="Immediate",
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]