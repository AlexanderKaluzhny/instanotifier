from instanotifier.parser.rss.utils import get_test_rss_feed_items
from instanotifier.notification.views import create_rssnotification_instances


def create_rssnotifications_from_test_feed():
    """ parse test feed and save notifications """

    feed_items = get_test_rss_feed_items()

    saved_pks = create_rssnotification_instances(feed_items)
    return saved_pks
