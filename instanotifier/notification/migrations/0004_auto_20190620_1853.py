# Generated by Django 2.2.2 on 2019-06-20 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_rssnotification_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rssnotification',
            name='internal_id',
            field=models.CharField(db_index=True, editable=False, max_length=255, unique=True, verbose_name='Internal entry id'),
        ),
    ]