# Generated by Django 3.0.7 on 2020-06-13 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0006_auto_20200613_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='email'),
        ),
    ]