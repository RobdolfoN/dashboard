# Generated by Django 4.0.5 on 2022-11-26 23:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dddashboard', '0008_alter_companydata_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydata',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dddashboard.companyname'),
        ),
    ]
