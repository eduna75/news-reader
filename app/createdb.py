__author__ = 'justus'

import sqlite3


def create_db(database):
    db = sqlite3.connect(database)
    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS news")
    cur.execute(
        "CREATE TABLE news(id INTEGER PRIMARY KEY, title VARCHAR UNIQUE, summary VARCHAR UNIQUE, "
        "link VARCHAR UNIQUE, timestamp DATETIME DEFAULT current_timestamp, publisher VARCHAR, source VARCHAR,"
        " date VARCHAR)")
    cur.execute("DROP TABLE IF EXISTS url")
    cur.execute("CREATE TABLE url(url_id INTEGER PRIMARY KEY, url VARCHAR UNIQUE, name VARCHAR NOT NULL, "
                "active INTEGER NOT NULL )")
    cur.execute("DROP TABLE IF EXISTS user")
    cur.execute("CREATE TABLE user(uid INTEGER PRIMARY KEY, fname VARCHAR NOT NULL, mname varchar, lname VARCHAR,"
                "bdate INTEGER, email VARCHAR NOT NULL, location VARCHAR, language VARCHAR, login_name VARCHAR NOT NULL,"
                " password VARCHAR NOT NULL, timestamp DATETIME DEFAULT current_timestamp, ip VARCHAR, theme VARCHAR, "
                "active VARCHAR, newsletter VARCHAR, admin VARCHAR)")
    cur.execute("DROP TABLE IF EXISTS log")
    cur.execute("CREATE TABLE log(loid VARCHAR INTEGER PRIMARY KEY, uid INTEGER NOT NULL, "
                "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, ip VARCHAR, ip_location VARCHAR, browser VARCHAR, "
                "system VARCHAR, news_red VARCHAR, read_more VARCHAR, language VARCHAR)")
    cur.execute("DROP TABLE IF EXISTS config")
    cur.execute("CREATE TABLE config(name_website VARCHAR, slogan VARCHAR, newsletter VARCHAR, system_theme VARCHAR)")
    db.commit()
    db.close()


def fill_url(database):
    db = sqlite3.connect(database)
    db.execute('INSERT INTO url(url, name, active) VALUES ("http://englishnews.thaipbs.or.th/feed", "Thai PBS", 1)')
    db.execute('INSERT INTO user(uid, fname, mname, lname, email, location, language, login_name, password, theme, '
               'active, admin) VALUES(1,"Justus","Franciscus","Ouwerling","eduna75@gmail.com","Thailand","English",'
               '"eduna75","qwerty","flatly",1,1 ) ')
    db.execute('INSERT INTO config(name_website, slogan, system_theme) VALUES ("Headlines", "The news from right now", '
               '"journal")')
    db.commit()
    db.close()


if __name__ == "__main__":
    create_db('news-reader.db')
    fill_url('news-reader.db')