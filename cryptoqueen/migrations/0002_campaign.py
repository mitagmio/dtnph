# Generated by Django 3.2.13 on 2022-08-12 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoqueen', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('name', models.CharField(max_length=33)),
                ('bot_url', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('target_url', models.CharField(blank=True, max_length=256, null=True)),
                ('ad_cost', models.FloatField(default=0)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]