# Generated by Django 4.2.4 on 2023-08-09 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_api', '0003_newsfeed'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
