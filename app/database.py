from views import sql_db
from data_models import NewsPost


# create the database
sql_db.create_all()


# insert
sql_db.session.add(NewsPost("Good", "not good"))
sql_db.session.add(NewsPost("bad", "not bad at all"))


# commit the change
sql_db.session.commit()