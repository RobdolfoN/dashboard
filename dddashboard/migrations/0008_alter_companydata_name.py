# Generated by Django 4.0.5 on 2022-11-26 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dddashboard', '0007_companydata_companyname_delete_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydata',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dddashboard.companyname'),
        ),
    ]
