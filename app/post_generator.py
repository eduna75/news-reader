__author__ = 'justus'

import feedparser
import sqlite3


def generator():

    link = sqlite3.connect('news-reader.db')
    links = link.execute('SELECT * FROM url')

    for l in links:
        feeds = feedparser.parse(l[1])
        db = sqlite3.connect('news-reader.db')
        for i in xrange(0, len(feeds['entries'])):
            try:
                post = [(feeds['entries'][i].title), (feeds['entries'][i].summary), (feeds['entries'][i].link)]
                print post, '\n'
            except BaseException as e:
                print 'could not extract everything', e
            try:
                db.execute('INSERT INTO news(title, summary, link) VALUES (?,?,?);', post)
                db.commit()
            except BaseException as e:
                print 'Double entry, was not committed to the database', e
        db.close()


if __name__ == "__main__":
    generator()