# Generated by Django 3.2.13 on 2022-06-21 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_time_payment', models.PositiveBigIntegerField(default=1651688047000)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='message_id',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='ref_id',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(default='0', max_length=32),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.PositiveBigIntegerField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('summ_invoice', models.FloatField(primary_key=True, serialize=False)),
                ('payer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payer_id_invoice_set', to='tgbot.user')),
            ],
        ),
    ]