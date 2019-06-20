from instanotifier.parser.rss.test_utils import get_test_rss_feed_items
from instanotifier.notification.views import create_rssnotification_instances
from instanotifier.notification.models import RssNotification


def create_rssnotifications_from_test_feed():
    """ parse test feed and save notifications """

    feed_items = get_test_rss_feed_items()

    saved_pks = create_rssnotification_instances(feed_items)
    return saved_pks


def delete_test_rss_feed_notifications():
    """ Finds all the rss test feed entries and deletes related RssNotification instances """

    feed_items = get_test_rss_feed_items()

    deleted_count = 0
    for item in feed_items:
        id_hash = RssNotification.compute_entry_id_hash(item["id"])
        try:
            obj = RssNotification.objects.get(internal_id=id_hash)
        except RssNotification.DoesNotExist:
            continue

        obj.delete()
        deleted_count += 1

    return deleted_count
