__author__ = 'justus'

from views import sql_db


class NewsPost(sql_db.Model):

    id = sql_db.Column(sql_db.Integer, primary_key=True)
    title = sql_db.Column(sql_db.String, nullable=False)
    summary = sql_db.Column(sql_db.String, nullable=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<title> {}'.format(self.title)