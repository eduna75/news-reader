from flask import session, flash, redirect, url_for
from functools import wraps


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first.")
            return redirect(url_for('index'))
    return wrap