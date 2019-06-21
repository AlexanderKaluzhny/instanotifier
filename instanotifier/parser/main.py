from instanotifier.parser.rss.parser import RssParser
from instanotifier.notification.views import create_rssnotification_instances


def parse(feed):
    parser = RssParser(feed)
    feed_info, feed_items = parser.parse()

    saved_pks = create_rssnotification_instances(feed_items)

    # TODO: take some general info from feed_info and update the FeedSource

    return saved_pks
