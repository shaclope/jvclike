# Generated by Django 5.0.6 on 2024-06-13 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="topic",
            name="created_by",
        ),
        migrations.AddField(
            model_name="topic",
            name="content",
            field=models.TextField(default="Default content"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="topic",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]