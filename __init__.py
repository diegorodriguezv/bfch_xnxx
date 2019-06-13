from chanutils import get_doc, select_all, select_one, get_attr, get_text, get_json
from playitem import PlayItem, PlayItemList
import lxml.etree

_SEARCH_URL = "https://xnxx.com/search/"
_ROOT_URL = "https://xnxx.com"
_FEEDLIST = [
    {'title': 'Compilation', 'url': '/search/compilation?top'},
    {'title': 'Cuckold', 'url': '/tags/cuckold'},
    {'title': 'Amateur', 'url': '/tags/amateur'},
    {'title': 'Public', 'url': '/tags/public'},
    {'title': 'Shemale', 'url': '/search/shemale'},
    {'title': 'Gay Porn', 'url': '/search/gay'},
    {'title': 'Taboo', 'url': '/search/taboo?top'},
    {'title': 'Lesbian', 'url': '/search/lesbian'},
    {'title': 'Big ass latina', 'url': '/search/big+ass+latina?top'},
    {'title': 'Mature Women', 'url': '/search/mature'},
    {'title': 'Stepmom and son', 'url': '/search/stepmom+and+son?top'},
    {'title': 'Black Girls', 'url': '/search/black_woman'},
    {'title': 'Sleeping', 'url': '/search/sleeping?top'},
    {'title': 'Anal Sex', 'url': '/search/anal'},
    {'title': 'Wife', 'url': '/search/wife?top'},
    {'title': 'Big Ass', 'url': '/search/big_ass'},
    {'title': 'Big black ass', 'url': '/search/big+black+ass?top'},
    {'title': 'BBW', 'url': '/search/bbw'},
    {'title': 'Real mom and son', 'url': '/search/real+mom+and+son?top'},
    {'title': 'REAL Amateur', 'url': '/search/real_amateur'},
    {'title': 'Young teen forced', 'url': '/search/young+teen+forced?top'},
    {'title': 'Creampie', 'url': '/search/creampie'},
    {'title': 'Chubby', 'url': '/search/chubby?top'},
    {'title': 'Milf', 'url': '/search/milf'},
    {'title': 'Son forced mom', 'url': '/search/son+forced+mom?top'},
    {'title': 'Big Tits', 'url': '/search/big_tits'},
    {'title': 'Hardcore', 'url': '/search/hardcore?top'},
    {'title': 'Latina', 'url': '/search/latina'},
    {'title': 'Pov', 'url': '/search/pov?top'},
    {'title': '18', 'url': '/search/teen'},
    {'title': 'Cheating wife', 'url': '/search/cheating+wife?top'},
    {'title': 'India / Indian girls', 'url': '/search/indian'},
    {'title': 'Hot milf', 'url': '/search/hot+milf?top'}
]


def name():
    return 'XNXX'


def image():
    return 'icon.png'


def description():
    return "XNXX Channel (<a target='_blank' href='https://xnxx.com'>https://xnxx.com</a>)."


def feedlist():
    return _FEEDLIST


def feed(idx):
    doc = get_doc(_ROOT_URL + _FEEDLIST[idx]['url'])
    return _extract(doc)


def _extract(doc):
    rtree = select_all(doc, 'div.thumb-block')
    results = PlayItemList()
    for l in rtree:
        ti = select_one(l, 'div.thumb-inside')
        ael = select_one(ti, 'a')
        url = _ROOT_URL + get_attr(ael, 'href')
        imgel = select_one(ael, 'img')
        img = get_attr(imgel, 'data-src')
        img = img.replace('THUMBNUM', '2')
        tu = select_one(l, 'div.thumb-under')
        el = select_one(tu, 'a')
        title = get_text(el)
        el = select_one(tu, 'p.metadata')
        lxml.etree.strip_tags(el, '*')
        strings = el.text.replace('\n', ' ').split(' ')
        strings = [x for x in strings if x.strip()]
        if len(strings) == 2:
            size = strings[0]
            rating = "NA"
            duration = strings[1]
        elif len(strings) == 3:
            size = strings[0]
            rating = strings[1]
            duration = strings[2]
        elif len(strings) == 4:
            size = strings[0]
            rating = strings[1]
            duration = strings[2] + " " + strings[3]
        subtitle = _subtitle(
            {'Duration': duration, 'Size': size, 'Rating': rating})
        results.add(PlayItem(title, img, url, subtitle))
    return results


def _subtitle(dict):
    return ', '.join(['%s: %s' % (key, value) for (key, value) in dict.items()])


def search(q):
    doc = get_doc(_SEARCH_URL + q)
    return _extract(doc)
