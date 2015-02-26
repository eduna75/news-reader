__author__ = 'justus'

import sqlite3


class DBConnect:

    def __init__(self):
        pass

    @staticmethod
    def db_connect():
        conn = sqlite3.connect('app/news-reader.db')
        return conn