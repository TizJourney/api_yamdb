# Generated by Django 3.0.5 on 2020-11-01 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_comment_review_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='yamdbuser',
            options={'ordering': ('-date_joined',)},
        ),
    ]
