import os
from flask import Flask
from apis import api
from models import db

my_app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(my_app.root_path, 'database/database.db')
my_app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(my_app)

api.init_app(my_app)

if __name__ == '__main__':
    my_app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
