# Generated by Django 4.0.5 on 2022-11-27 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dddashboard', '0010_rename_name_companydata_comany_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companydata',
            old_name='comany_name',
            new_name='company_name',
        ),
    ]
