from django.db import migrations, models
from bs4 import BeautifulSoup


def _parse_country(summary):
    soup = BeautifulSoup(summary, features="html5lib")
    country_tag = soup.find(text="Country")
    if country_tag:
        country = country_tag.find_next(string=True).strip(': \n')
        return country
    return "Unknown"


def populate_country_column(apps, schema_editor):
    """
    Populates the `country` column by parsing it from the `summary` for all existing instances
    """
    Model = apps.get_model('notification', 'RssNotification')
    for instance in Model.objects.all():
        country = _parse_country(instance.summary)
        instance.country = country
        instance.save(update_fields=['country'])


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0006_auto_20190911_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='rssnotification',
            name='country',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.RunPython(populate_country_column),
    ]
