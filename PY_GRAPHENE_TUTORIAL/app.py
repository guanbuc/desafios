# -*- encoding:utf-8 -*-


from api import app
from database import db_session, init_db


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run()