import time
from app.login.models import Feed, User
import feedparser
from app.db_connect import DBConnect as DBc


def time_ago(data):
    t = time.localtime()
    p = data
    posted = int((time.mktime(t) - time.mktime(p)) / 60 / 60)
    return posted


def fetch(urls):
    feed = []
    for links in urls[0:2]:
        feeds = feedparser.parse(links.url)
        for i in xrange(0, len(feeds.entries)):
            entries = {'title': feeds.entries[i].title, 'summary': feeds.entries[i].summary,
                       'link': feeds.entries[i].link, 'published': feeds.entries[i].published,
                       'publisher': feeds.feed.title, 'published_parsed': time_ago(feeds.entries[i].published_parsed)}
            feed.append(entries)

    return feed


def logon(user_id):
    urls = []
    feeds = Feed.query.join(User.urls).filter(User.id == user_id).all()
    if not feeds:
        feeds = Feed.query.filter_by(id=1).all()
    for feed in feeds:
        urls.append(feed)
    return fetch(urls)


if __name__ == "__main__":
    pass