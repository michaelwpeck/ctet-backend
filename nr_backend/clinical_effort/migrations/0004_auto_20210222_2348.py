# Generated by Django 3.1.7 on 2021-02-23 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinical_effort', '0003_auto_20210222_1836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cycles',
            old_name='heading',
            new_name='name',
        ),
    ]
