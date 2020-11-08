# Generated by Django 3.0.5 on 2020-11-08 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20201108_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yamdbuser',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')], default='user', max_length=9),
        ),
    ]
