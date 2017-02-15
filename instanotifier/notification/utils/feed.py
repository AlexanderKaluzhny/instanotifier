from instanotifier.parser.rss.utils import get_test_rss_feed_items
from instanotifier.notification.models import RssNotification


def delete_test_rss_feed_notifications():
    """ Finds all the rss test feed entries and deletes related RssNotification instances """

    feed_items = get_test_rss_feed_items()

    deleted_count = 0
    for item in feed_items:
        id_hash = RssNotification.compute_internal_id_hash(item['id'])
        try:
            obj = RssNotification.objects.get(internal_id=id_hash)
            if obj:
                obj.delete()
                deleted_count += 1
        except RssNotification.DoesNotExist:
            pass

    return deleted_count

def get_item_field(feed_items, item_idx, field_name):

    if not len(feed_items) or not isinstance(feed_items, list):
        raise ValueError("Invalid feed specified.")

    item = feed_items[item_idx]

    try:
        value = item[field_name]
    except KeyError:
        raise KeyError("No key %s in %s." % (field_name, item.keys()))

    return value

def get_test_feed_item_field(item_idx, field_name, feed_path=None):
    feed_items = get_test_rss_feed_items()

    return get_item_field(feed_items, item_idx, field_name)
