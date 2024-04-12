# Generated by Django 3.2 on 2024-02-18 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='industry',
            field=models.CharField(choices=[('technology', 'Technology'), ('finance', 'Finance'), ('healthcare', 'Healthcare'), ('manufacturing', 'Manufacturing'), ('retail', 'Retail'), ('hospitality', 'Hospitality'), ('blue collar', 'Blue Collar'), ('real estate', 'Real Estate'), ('energy', 'Energy'), ('food processing', 'Food Processing'), ('public service', 'Public Service'), ('non profit', 'Non Profit'), ('transportation & logistics', 'Transportation & Logistics'), ('waste management', 'Waste Management'), ('telecommunications', 'Telecommunications'), ('media & entertainment', 'Media & Entertainment'), ('construction & engineering', 'Construction & Engineering'), ('agriculture', 'Agriculture'), ('education', 'Education'), ('professional services', 'Professional Services'), ('mining', 'Mining'), ('pharmaceutical', 'Pharmaceutical')], default='energy', max_length=50),
        ),
        migrations.AlterField(
            model_name='tag',
            name='topic',
            field=models.CharField(choices=[('technology', 'Technology'), ('finance', 'Finance'), ('healthcare', 'Healthcare'), ('manufacturing', 'Manufacturing'), ('retail', 'Retail'), ('hospitality', 'Hospitality'), ('blue collar', 'Blue Collar'), ('real estate', 'Real Estate'), ('energy', 'Energy'), ('food processing', 'Food Processing'), ('public service', 'Public Service'), ('non profit', 'Non Profit'), ('transportation & logistics', 'Transportation & Logistics'), ('waste management', 'Waste Management'), ('telecommunications', 'Telecommunications'), ('media & entertainment', 'Media & Entertainment'), ('construction & engineering', 'Construction & Engineering'), ('agriculture', 'Agriculture'), ('education', 'Education'), ('professional services', 'Professional Services'), ('mining', 'Mining'), ('pharmaceutical', 'Pharmaceutical')], default='energy', max_length=50),
        ),
    ]
