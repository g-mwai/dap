# Generated by Django 3.2 on 2024-02-19 07:20

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('moderation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='body',
            field=tinymce.models.HTMLField(),
        ),
    ]
