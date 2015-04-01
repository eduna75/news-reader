import feedparser
from app.db_connect import DBConnect as DBc


def generator():
    link = DBc.db_connect()
    links = link.execute('SELECT * FROM url')
    total_committed = 0
    total_double = 0
    for l in links:
        url_id = l[0]
        feeds = feedparser.parse(l[1])
        for i in xrange(0, len(feeds['entries'])):
            try:
                post = [feeds['entries'][i].title, feeds['entries'][i].summary, feeds['entries'][i].link,
                        feeds['feed'].title, url_id, feeds['entries'][i].published]
                print post, '\n'
            except BaseException as e:
                print 'could not extract everything', e
            try:
                link.execute('INSERT INTO news(title, summary, link, publisher, source, date) VALUES (?,?,?,?,?,?);',
                             post)
                link.commit()
                total_committed += 1
            except BaseException as e:
                print 'Double entry, was not committed to the database', e
                total_double += 1
    return total_committed
    link.close()


def fetch(urls):
    feed = []
    for l in urls:
        feeds = feedparser.parse(l)
        for i in xrange(0, len(feeds['entries'])):
            entries = {'title': feeds['entries'][i].title, 'summary': feeds['entries'][i].summary,
                       'link': feeds['entries'][i].link, 'f_title': feeds['feed'].title,
                       'published': feeds['entries'][i].published}
            feed.append(entries)

    return feed


def logon():
    feeds = ('http://englishnews.thaipbs.or.th/feed', 'http://www.bangkokpost.com/rss/data/topstories.xml')
    return fetch(feeds)

if __name__ == "__main__":
    pass