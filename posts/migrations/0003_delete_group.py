# Generated by Django 2.2.9 on 2021-03-13 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_group'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Group',
        ),
    ]