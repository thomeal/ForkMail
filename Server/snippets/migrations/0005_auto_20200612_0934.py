# Generated by Django 3.0.7 on 2020-06-12 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0004_auto_20200612_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='imap_host',
            field=models.CharField(max_length=50, verbose_name='imap_host'),
        ),
        migrations.AlterField(
            model_name='email',
            name='imap_port',
            field=models.CharField(max_length=50, verbose_name='imap_port'),
        ),
        migrations.AlterField(
            model_name='email',
            name='smtp_host',
            field=models.CharField(max_length=50, verbose_name='smtp_host'),
        ),
        migrations.AlterField(
            model_name='email',
            name='smtp_port',
            field=models.CharField(max_length=50, verbose_name='smtp_port'),
        ),
    ]
