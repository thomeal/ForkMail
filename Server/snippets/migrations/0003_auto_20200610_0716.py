# Generated by Django 3.0.7 on 2020-06-10 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_auto_20200610_0654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='sex',
            new_name='password',
        ),
    ]
