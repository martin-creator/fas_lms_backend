# Generated by Django 5.0.6 on 2024-06-13 20:18

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("activity", "0003_initial"),
        ("companies", "0002_initial"),
        ("jobs", "0001_initial"),
        ("profiles", "0001_initial"),
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplication",
            name="applicant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="applications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="shares",
            field=models.ManyToManyField(
                blank=True, related_name="shared_applications", to="activity.share"
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="applications",
            field=models.ManyToManyField(
                blank=True,
                db_index=True,
                related_name="applications_job_listings",
                to="jobs.jobapplication",
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="categories",
            field=models.ManyToManyField(
                related_name="job_listings_categories", to="activity.category"
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_listings_companies",
                to="companies.company",
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="shares",
            field=models.ManyToManyField(
                blank=True, related_name="shared_job_listings", to="activity.share"
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="skills_required",
            field=models.ManyToManyField(
                blank=True,
                db_index=True,
                related_name="required_jobs",
                to="profiles.skill",
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
        migrations.AddField(
            model_name="jobapplication",
            name="job_listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_applications",
                to="jobs.joblisting",
            ),
        ),
        migrations.AddField(
            model_name="jobnotification",
            name="job_listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="job_notifications",
                to="jobs.joblisting",
            ),
        ),
        migrations.AddField(
            model_name="jobnotification",
            name="shares",
            field=models.ManyToManyField(
                blank=True, related_name="shared_notifications", to="activity.share"
            ),
        ),
        migrations.AddField(
            model_name="jobnotification",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="notifications",
            field=models.ManyToManyField(
                blank=True,
                db_index=True,
                related_name="notifications_job_listings",
                to="jobs.jobnotification",
            ),
        ),
    ]
