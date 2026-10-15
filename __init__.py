import re

import lxml.etree

from lib.chanutils import get_attr, get_doc, get_text, select_all, select_one
from lib.playitem import PlayItem, PlayItemList

# The site redirects the bare host to www on every request, and /tags/* to
# /search/*. Going straight to where it lands saves a redirect per feed.
_ROOT_URL = "https://www.xnxx.com"
_SEARCH_URL = _ROOT_URL + "/search/"

_FEEDLIST = [
    # Three feeds were here and are not any more: "Sleeping", "Young teen
    # forced" and "Son forced mom".
    #
    # The site answers 404 for those three terms now, so each of those feeds was
    # an error page rather than a list of videos. It is the term and not the
    # "top" parameter -- all three answer 404 with that parameter dropped, while
    # the other thirty answer 200 either way.
    #
    # They are not repointed at a term that does answer. A feed titled "Sleeping"
    # that quietly returned something else would be worse than a missing feed:
    # it looks like it works. Search is still there, and a term the site will
    # answer can still be typed into it.
    #
    # The first two also name material involving minors, which is a category the
    # site now declines to search. Whatever the reason for any one of them, a
    # feed that cannot return results is a feed that does not belong in a menu.
    {"title": "Compilation", "url": "/search/compilation?top"},
    {"title": "Cuckold", "url": "/tags/cuckold"},
    {"title": "Amateur", "url": "/tags/amateur"},
    {"title": "Public", "url": "/tags/public"},
    {"title": "Shemale", "url": "/search/shemale"},
    {"title": "Gay Porn", "url": "/search/gay"},
    {"title": "Taboo", "url": "/search/taboo?top"},
    {"title": "Lesbian", "url": "/search/lesbian"},
    {"title": "Big ass latina", "url": "/search/big+ass+latina?top"},
    {"title": "Mature Women", "url": "/search/mature"},
    {"title": "Stepmom and son", "url": "/search/stepmom+and+son?top"},
    {"title": "Black Girls", "url": "/search/black_woman"},
    {"title": "Anal Sex", "url": "/search/anal"},
    {"title": "Wife", "url": "/search/wife?top"},
    {"title": "Big Ass", "url": "/search/big_ass"},
    {"title": "Big black ass", "url": "/search/big+black+ass?top"},
    {"title": "BBW", "url": "/search/bbw"},
    {"title": "Real mom and son", "url": "/search/real+mom+and+son?top"},
    {"title": "REAL Amateur", "url": "/search/real_amateur"},
    {"title": "Creampie", "url": "/search/creampie"},
    {"title": "Chubby", "url": "/search/chubby?top"},
    {"title": "Milf", "url": "/search/milf"},
    {"title": "Big Tits", "url": "/search/big_tits"},
    {"title": "Hardcore", "url": "/search/hardcore?top"},
    {"title": "Latina", "url": "/search/latina"},
    {"title": "Pov", "url": "/search/pov?top"},
    {"title": "18", "url": "/search/teen"},
    {"title": "Cheating wife", "url": "/search/cheating+wife?top"},
    {"title": "India / Indian girls", "url": "/search/indian"},
    {"title": "Hot milf", "url": "/search/hot+milf?top"},
]

# How a token under p.metadata is recognised, rather than which position it
# happens to sit in.
#
# The original read the metadata as a fixed list and branched on how many
# words it found -- two words means views and length, three adds a rating, four
# splits the length. That works right up until the site adds a word, and it has:
# the HD marker arrived as " - 1080p", so the usual line went from three words to
# five. There was no branch for five, so `duration` was never assigned and the
# feed died with UnboundLocalError. Every feed and every search failed.
#
# Matching each word by shape instead means an added word is read for what it is
# and ignored if it is nothing we know about, so the next such change costs
# nothing.
_LENGTH_RE = re.compile(r"^(?:\d+h(?:\d+(?:min|sec)s?)?|\d+(?:min|sec)s?)$", re.I)
_QUALITY_RE = re.compile(r"^\d{3,4}p$", re.I)
_VIEWS_RE = re.compile(r"^[\d.]+[KMB]$", re.I)
_RATING_RE = re.compile(r"^\d+%$")

#: Shown for a value the page did not give, rather than left blank.
_UNKNOWN = "NA"


def name():
    return "XNXX"


def image():
    return "icon.png"


def description():
    return "XNXX Channel (<a target='_blank' href='https://xnxx.com'>https://xnxx.com</a>)."


def feedlist():
    return _FEEDLIST


def feed(idx):
    return _extract(_listing(_ROOT_URL + _FEEDLIST[idx]["url"]))


def search(q):
    return _extract(_listing(_SEARCH_URL + q))


def _listing(url):
    """
    Fetch a listing page, or nothing at all.

    The site answers 404 for some terms outright, and a search term is something
    the person searching chose -- so a term it declines is an ordinary outcome,
    not a fault. Raised, it came back as a 500 carrying a stack trace, which the
    interface has no way to explain and shows raw.

    A listing page that could not be read has no videos in it, and the interface
    already has a line for exactly that: "There are no results for this query."
    Letting the empty list reach it is the honest answer here -- the search did
    return nothing -- and it is the answer the interface was built to give.

    The failure is still written to the log. On screen an empty list and a
    request that never happened look identical, so without this a channel that
    stopped working for some reason other than having no videos would look like
    a channel with nothing in it and nothing to investigate.
    """
    try:
        return get_doc(url)
    except Exception as exc:
        print(f"bfch_xnxx: {url} could not be read ({exc.__class__.__name__})")
        return None


def _extract(doc):
    results = PlayItemList()
    if doc is None:
        return results
    for block in select_all(doc, "div.thumb-block"):
        item = _item(block)
        # One malformed card should cost that card, not the whole feed.
        if item is not None:
            results.add(item)
    return results


def _item(block):
    inside = select_one(block, "div.thumb-inside")
    under = select_one(block, "div.thumb-under")
    if inside is None or under is None:
        return None
    anchor = select_one(inside, "a")
    if anchor is None:
        return None
    href = get_attr(anchor, "href")
    if not href:
        return None
    url = href if href.startswith("http") else _ROOT_URL + href

    img = ""
    img_el = select_one(anchor, "img")
    if img_el is not None:
        img = get_attr(img_el, "data-src") or ""
        # The site serves a placeholder at this size and the real thumbnail at
        # the next one up.
        img = img.replace("THUMBNUM", "2")

    title_el = select_one(under, "a")
    title = get_text(title_el).strip() if title_el is not None else ""
    return PlayItem(title, img, url, _subtitle(block))


def _subtitle(block):
    length = quality = views = rating = _UNKNOWN
    for token in _tokens(block):
        if _LENGTH_RE.match(token):
            length = token
        elif _QUALITY_RE.match(token):
            quality = token
        elif _VIEWS_RE.match(token):
            views = token
        elif _RATING_RE.match(token):
            rating = token

    fields = [("Length", length), ("Views", views), ("Rating", rating)]
    if quality != _UNKNOWN:
        fields.append(("Quality", quality))
    return ", ".join("%s: %s" % (k, v) for k, v in fields)


def _tokens(block):
    """
    The words under a video card, flattened and split.

    strip_tags first: the metadata is wrapped in spans, so the text of interest
    is in the children's .text and el.text alone can be None.
    """
    meta = select_one(block, "p.metadata")
    if meta is None:
        return []
    lxml.etree.strip_tags(meta, "*")
    text = meta.text or ""
    # "-" is the separator the HD marker arrived with, not a value.
    return [
        t for t in text.replace("\n", " ").split(" ") if t.strip() and t.strip() != "-"
    ]
