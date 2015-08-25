from chanutils import get_doc, select_all, select_one, get_attr, get_text
from playitem import PlayItem, PlayItemList

_SEARCH_URL = "https://xnxx.com"

_FEEDLIST = [
  {'title':'18', 'url':'http://www.xnxx.com/c/Teen-13'},
  {'title':'Amateur', 'url':'http://www.xnxx.com/c/Amateur-17'},
  {'title':'American', 'url':'http://www.xnxx.com/tags/american'},
  {'title':'Anal Sex', 'url':'http://www.xnxx.com/c/Anal-12'},
  {'title':'Anime', 'url':'http://www.xnxx.com/c/Anime-41'},
  {'title':'Arab/Arabian', 'url':'http://www.xnxx.com/tags/arab'},
  {'title':'Asian Woman', 'url':'http://www.xnxx.com/c/Asian%20Woman-32'},
  {'title':'Ass', 'url':'http://www.xnxx.com/c/Ass-14'},
  {'title':'Ass gaping', 'url':'http://www.xnxx.com/tags/gape'},
  {'title':'Ass to Mouth', 'url':'http://www.xnxx.com/c/Ass%20to%20Mouth-29'},
  {'title':'Ass Fucked', 'url':'http://www.xnxx.com/c/Anal-12'},
  {'title':'Babysitter', 'url':'http://www.xnxx.com/tags/babysitter'},
  {'title':'BBW', 'url':'http://www.xnxx.com/c/bbw-51'},
  {'title':'BDSM', 'url':'http://www.xnxx.com/c/BDSM-44'},
  {'title':'Beach Sex', 'url':'http://www.xnxx.com/tags/beach'},
  {'title':'Big Ass', 'url':'http://www.xnxx.com/c/Big%20ass-24'},
  {'title':'Big Cock', 'url':'http://www.xnxx.com/c/big%20cock-34'},
  {'title':'Big Girl', 'url':'http://www.xnxx.com/c/bbw-51'},
  {'title':'Big Tits', 'url':'http://www.xnxx.com/c/big%20tits-23'},
  {'title':'Black Girls', 'url':'http://www.xnxx.com/c/Black%20Woman-30'},
  {'title':'Black Hair', 'url':'http://www.xnxx.com/c/Brunette-25'},
  {'title':'Blonde', 'url':'http://www.xnxx.com/c/Blonde-20'},
  {'title':'Blowjob', 'url':'http://www.xnxx.com/c/Blowjob-15'},
  {'title':'Bondage', 'url':'http://www.xnxx.com/tags/bondage'},
  {'title':'Brazilian', 'url':'http://www.xnxx.com/tags/brazilian'},
  {'title':'Brunette', 'url':'http://www.xnxx.com/c/Brunette-25'},
  {'title':'Butt', 'url':'http://www.xnxx.com/c/Ass-14'},
  {'title':'Cam Videos', 'url':'http://www.xnxx.com/tags/webcam'},
  {'title':'Casting', 'url':'http://www.xnxx.com/tags/casting'},
  {'title':'Chubby', 'url':'http://www.xnxx.com/tags/chubby'},
  {'title':'Classic View', 'url':'http://multi.xnxx.com/'},
  {'title':'Classic Porn', 'url':'http://www.xnxx.com/tags/classic'},
  {'title':'Clips(small)', 'url':'http://multi.xnxx.com/3thumbs/movie/d/on/small/all/index.html'},
  {'title':'College', 'url':'http://www.xnxx.com/tags/college'},
  {'title':'Compilation', 'url':'http://www.xnxx.com/tags/compilation'},
  {'title':'Creampie', 'url':'http://www.xnxx.com/c/Creampie-40'},
  {'title':'Cumshot', 'url':'http://www.xnxx.com/c/Cumshot-18'},
  {'title':'Deepthroat', 'url':'http://www.xnxx.com/tags/deepthroat'},
  {'title':'Doctor', 'url':'http://www.xnxx.com/tags/doctor'},
  {'title':'Ebony', 'url':'http://www.xnxx.com/c/Black%20Woman-30'},
  {'title':'Ex-Girlfriend', 'url':'http://www.xnxx.com/tags/girlfriend'},
  {'title':'Exhibitionism', 'url':'http://www.xnxx.com/tags/public'},
  {'title':'Fat', 'url':'http://www.xnxx.com/tags/fat'},
  {'title':'Female Ejaculation', 'url':'http://www.xnxx.com/tags/squirting'},
  {'title':'Fisting / Fist-Fucking', 'url':'http://www.xnxx.com/tags/fisting'},
  {'title':'French / France', 'url':'http://www.xnxx.com/tags/french'},
  {'title':'Fucked / Fucking', 'url':'http://www.xnxx.com/tags/fucked'},
  {'title':'Gagging', 'url':'http://www.xnxx.com/tags/gagging'},
  {'title':'Galleries', 'url':'http://multi.xnxx.com/'},
  {'title':'Gangbang', 'url':'http://www.xnxx.com/tags/gangbang'},
  {'title':'Gape/Gapping', 'url':'http://www.xnxx.com/tags/gaping'},
  {'title':'Gay Porn', 'url':'http://www.xnxx.com/c/Gay-45'},
  {'title':'German', 'url':'http://www.xnxx.com/tags/german'},
  {'title':'Girlfriend', 'url':'http://www.xnxx.com/tags/girlfriend'},
  {'title':'Granny', 'url':'http://www.xnxx.com/tags/granny'},
  {'title':'Hairy Pussy', 'url':'http://www.xnxx.com/tags/hairy'},
  {'title':'Handjob', 'url':'http://www.xnxx.com/tags/handjob'},
  {'title':'Hardcore', 'url':'http://www.xnxx.com/c/Hardcore-35'},
  {'title':'Heels', 'url':'http://www.xnxx.com/c/Heels-43'},

]
def name():
  return 'XNXX'

def image():
  return 'icon.png'

def description():
  return "XNXX Channel (<a target='_blank' href='https://xnxx.com'>https://xnxx.com/a>)."

def feedlist():
  return _FEEDLIST

def feed(idx):
  doc = get_doc(_FEEDLIST[idx]['url'])
  rtree = select_all(doc, 'div.thumbs li')
  results = PlayItemList()
  for l in rtree:
    el = select_one(l, 'a')
    url = get_attr(el, 'href')
    el = select_one(l, 'img')
    img = get_attr(el, 'src')
    el = select_one(l, 'h4.talk-link__speaker')
    subtitle = get_text(el)
    el = select_one(l, 'a span')
    title = get_text(el)
    results.add(PlayItem(title, img, url, subtitle))
  return results

def search(q):
  data = get_json(_SEARCH_URL, params={'q':q}, proxy=True)
  if not 'list' in data:
    return []
  rtree = data['list']
  results = PlayItemList()
  for r in rtree:
    cat = r['category']
    if not (cat in _CAT_WHITELIST):
      continue
    title = replace_entity(r['title'])
    subs = None
    if cat == 'Movies':
      subs = movie_title_year(title)
    elif cat == 'TV':
      subs = series_season_episode(title)
    img = '/img/icons/film.svg'
    if cat == 'Music':
      img = '/img/icons/music.svg'
    size = byte_size(r['size'])
    subtitle = chanutils.torrent.subtitle(size, r['seeds'], r['peers'])
    url = r['torrentLink']
    results.add(TorrentPlayItem(title, img, url, subtitle, subs=subs))
  return results

