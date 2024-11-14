# Generated by Django 5.1.2 on 2024-11-14 16:40

import ptn_project.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptn_project', '0015_aifeedbacksummary_upload_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussionimage',
            name='image',
            field=models.ImageField(null=True, upload_to=ptn_project.models.discussion_image_upload_path),
        ),
        migrations.AlterField(
            model_name='feedbackimage',
            name='image',
            field=models.ImageField(null=True, upload_to=ptn_project.models.feedback_image_upload_path),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_thumbnail',
            field=models.ImageField(default='default.png', null=True, upload_to=ptn_project.models.thumbnail_upload_path),
        ),
        migrations.AlterField(
            model_name='projectimage',
            name='image',
            field=models.ImageField(null=True, upload_to=ptn_project.models.detail_image_upload_path),
        ),
    ]