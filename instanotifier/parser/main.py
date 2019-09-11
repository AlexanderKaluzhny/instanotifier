from instanotifier.parser.rss.parser import RssParser
from instanotifier.notification.views import create_rssnotification_instances


def parse(feed):
    parser = RssParser(feed)
    feed_info, feed_items = parser.parse()

    return feed_info, feed_items


def parse_and_save(feed, feed_source):
    feed_info, feed_items = parse(feed)

    saved_pks = create_rssnotification_instances(feed_items, feed_source)
    return saved_pks
