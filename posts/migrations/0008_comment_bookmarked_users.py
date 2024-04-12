# Generated by Django 3.2 on 2024-03-16 08:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0007_auto_20240314_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='bookmarked_users',
            field=models.ManyToManyField(blank=True, related_name='bookmarked_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
