__author__ = 'justus'

import sqlite3


class DBConnect:

    def __init__(self):
        pass

    @staticmethod
    def db_connect():
        conn = sqlite3.connect('news-reader.db')
        return conn

    def con_config(self):
        conf_db = self.db_connect()
        config = conf_db.execute('SELECT * FROM config')
        site_config = [dict(title=row[0], slogan=row[1], theme=row[3]) for row in config.fetchall()]
        conf_db.close()
        return site_config