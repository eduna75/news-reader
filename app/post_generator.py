import time
from app.login.models import Feed
import feedparser
import re


def time_ago(data):
    t = time.localtime()
    p = data
    posted = int((time.mktime(t) - time.mktime(p)) / 60 / 60)
    return posted


def fetch(urls):
    feed = []
    for links in urls[0:1]:
        feeds = feedparser.parse(links.url)
        for i in xrange(0, len(feeds.entries)):
            image = None
            value = str(feeds.entries[i].links)
            try:
                image_url = re.search('(?P<url>http?://[^\s]+(png|jpeg|jpg))', value).group("url")
                if 'NoneType' in image_url:
                    image = None
                else:
                    image = image_url
            except BaseException as e:
                print e

            entries = {'title': feeds.entries[i].title, 'summary': feeds.entries[i].summary,
                       'link': feeds.entries[i].link, 'published': feeds.entries[i].published,
                       'publisher': feeds.feed.title, 'published_parsed': time_ago(feeds.entries[i].published_parsed),
                       'image': image}
            feed.append(entries)

    return feed


def post(url=None):
    # next is used for as user has no feeds yet.
    if not url:
        url = Feed.query.filter_by(id=1).all()
    return fetch(url)


if __name__ == "__main__":
    pass