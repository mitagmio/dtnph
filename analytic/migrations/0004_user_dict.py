# Generated by Django 3.2.13 on 2022-08-12 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytic', '0003_alter_campaign_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='dict',
            field=models.TextField(blank=True, null=True),
        ),
    ]
