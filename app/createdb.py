__author__ = 'justus'

import sqlite3


def create_db(database):
    db = sqlite3.connect(database)
    cur = db.cursor()
    cur.execute(
        "CREATE TABLE news(id INTEGER PRIMARY KEY, title VARCHAR UNIQUE, summary VARCHAR UNIQUE, "
        "link VARCHAR UNIQUE, timestamp DATETIME DEFAULT current_timestamp, publisher VARCHAR, source VARCHAR)")
    cur.execute("CREATE TABLE url(url_id INTEGER PRIMARY KEY, url VARCHAR UNIQUE, name VARCHAR NOT NULL, "
                "active INTEGER NOT NULL )")
    db.commit()
    db.close()


def fill_url(database):
    db = sqlite3.connect(database)
    db.execute('INSERT INTO url(url, name) VALUES ("http://englishnews.thaipbs.or.th/feed", "Thai PBS")')
    db.commit()
    db.close()


if __name__ == "__main__":
    fill_url('news-reader.db')
    # create_db('news-reader.db')