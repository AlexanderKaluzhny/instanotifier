from instanotifier.parser.rss import utils

"""
Necessary feed info fields: feed_object['feed'].keys()
"""
RSS_FEED_INFO_FIELDS = [u"title", u"link", u"author", u"published_parsed", u"generator"]
"""
Necessary feed info fields: feed_object['entries'][ii].keys()
"""
RSS_FEED_ENTRY_FIELDS = [
    u"title",
    u"summary",
    u"link",
    u"published_parsed",
    u"id",  # hash or leave as is
]


class RssParser(object):
    """ Parses RSS feed fetched by the RssFetcher. """

    feed_info_key = "feed"
    feed_entries_key = "entries"

    def __init__(self, feed):
        self.feed = feed

    def parse_feed_info(self, feed):
        feed = feed.get(self.feed_info_key, None)
        if not feed:
            raise ValueError("Empty info feed specified")

        feed_info = utils.filter_feed_by_fields(feed, RSS_FEED_INFO_FIELDS)

        return feed_info

    def parse_feed_items(self, feed):
        feed_entries = feed.get(self.feed_entries_key, None)
        if not feed_entries:
            raise ValueError("Feed with no entries specified")

        feed_items = list()
        for entry in feed_entries:
            item = utils.filter_feed_by_fields(entry, RSS_FEED_ENTRY_FIELDS)
            feed_items.append(item)

        if len(feed_items):
            # FIXME: TODO: handle serialization of items in the Parser
            assert type(feed_items[0]["published_parsed"]) is unicode

        return feed_items

    def parse(self):
        if self.feed["bozo"]:
            # feed parsing error occurred.
            # TODO: handle exceptions. Pass wrong file path into feedparser to get an exception.

            # exception_content = {
            #     "exception": str(type(self.feed['bozo_exception'])),
            #     "content": str(self.feed['bozo_exception'].getException()),
            #     "line": self.feed['bozo_exception'].getLineNumber(),
            #     "message": self.feed['bozo_exception'].getMessage(),
            # }
            # feed['bozo_exception'] = exception_content
            pass
        else:
            feed_info = self.parse_feed_info(self.feed)
            feed_items = self.parse_feed_items(self.feed)

            return feed_info, feed_items
