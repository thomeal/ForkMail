# Generated by Django 3.0.7 on 2020-06-18 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0008_auto_20200617_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='imap_host',
            field=models.CharField(max_length=50, null=True, verbose_name='imap_host'),
        ),
        migrations.AddField(
            model_name='email',
            name='imap_port',
            field=models.CharField(max_length=50, null=True, verbose_name='imap_port'),
        ),
        migrations.AddField(
            model_name='email',
            name='smtp_host',
            field=models.CharField(max_length=50, null=True, verbose_name='smtp_host'),
        ),
        migrations.AddField(
            model_name='email',
            name='smtp_port',
            field=models.CharField(max_length=50, null=True, verbose_name='smtp_port'),
        ),
    ]
