# Generated by Django 2.2.2 on 2020-06-17 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0008_rssnotification_modified_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssnotification',
            name='is_bookmarked',
            field=models.BooleanField(default=False),
        ),
    ]