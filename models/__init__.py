import os
from xmlrpc.client import Boolean
from flask_sqlalchemy import SQLAlchemy
import os
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy(session_options={"autoflush": True})


def create_database(forced_delete=False):

    if not os.path.exists("..database/database.db") or forced_delete:
        db.create_all()
