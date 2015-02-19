__author__ = 'justus'

import feedparser
import sqlite3


def generator():

    link = sqlite3.connect('news-reader.db')
    links = link.execute('SELECT * FROM url')
    total_committed = 0
    total_double = 0
    for l in links:
        feeds = feedparser.parse(l[1])
        for i in xrange(0, len(feeds['entries'])):
            try:
                post = [(feeds['entries'][i].title), (feeds['entries'][i].summary), (feeds['entries'][i].link), (feeds['feed'].title), (feeds['entries'][i].published)]
                print post, '\n'
            except BaseException as e:
                print 'could not extract everything', e
            try:
                link.execute('INSERT INTO news(title, summary, link, publisher, date) VALUES (?,?,?,?,?);', post)
                link.commit()
                total_committed += 1
            except BaseException as e:
                print 'Double entry, was not committed to the database', e
                total_double += 1
    print total_double
    print total_committed
    link.close()


if __name__ == "__main__":
    generator()