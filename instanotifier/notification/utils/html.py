import html5lib
from html5lib import serializer, treebuilders, treewalkers


def _get_default_parser():
    opts = {}
    return html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"), **opts)


DEFAULT_PARSER = _get_default_parser()


def clean_html(data, full=False, parser=DEFAULT_PARSER):
    """
    Cleans HTML from XSS vulnerabilities using html5lib
    If full is False, only the contents inside <body> will be returned (without
    the <body> tags).
    """
    if full:
        dom_tree = parser.parse(data)
    else:
        dom_tree = parser.parseFragment(data)
    walker = treewalkers.getTreeWalker("dom")
    stream = walker(dom_tree)
    s = serializer.HTMLSerializer(
        omit_optional_tags=False, quote_attr_values="always", sanitize=True
    )
    return u"".join(s.serialize(stream))
