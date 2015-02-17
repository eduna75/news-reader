__author__ = 'justus'

import feedparser
import sqlite3


def generator():
    links = [
        'http://www.nationmultimedia.com/home/rss/breakingnews.rss',
        'http://www.bangkokpost.com/rss/data/most-recent.xml',
        'http://www.nationmultimedia.com/home/rss/breakingnews.rss',
        'http://www.nationmultimedia.com/home/rss/national.rss'
        ]

    for l in links:
        feed = feedparser.parse(l)
        db = sqlite3.connect('news-reader.db')
        for i in xrange(0, len(feed['entries'])):
            post = [(feed['entries'][i].title), (feed['entries'][i].summary), (feed['entries'][i].link)]
            print post, '\n'
            try:
                db.execute('INSERT INTO news(title, summary, link) VALUES (?,?,?);', post)
                db.commit()
            except BaseException as e:
                print 'Double entry, was not committed to the database', e
        db.close()

if __name__ == "__main__":
    generator()