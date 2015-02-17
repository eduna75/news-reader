__author__ = 'justus'

import sqlite3


def create_db(database):
    db = sqlite3.connect(database)
    cur = db.cursor()
    cur.execute(
        """CREATE TABLE news(id INTEGER PRIMARY KEY, title VARCHAR UNIQUE, summary VARCHAR UNIQUE, link VARCHAR UNIQUE)""")
    db.commit()
    db.close()

if __name__ == "__main__":
    create_db('news-reader.db')