# Generated by Django 3.2 on 2024-03-02 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='profile_pics/default_avatar.jpg', null=True, upload_to='profile_pics/'),
        ),
    ]
