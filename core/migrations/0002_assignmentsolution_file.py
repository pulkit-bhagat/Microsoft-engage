# Generated by Django 2.2.6 on 2021-11-22 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsolution',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]