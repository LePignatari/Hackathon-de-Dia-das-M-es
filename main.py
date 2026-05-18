from flask import Flask
from db import db
from models.users import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SECRET_KEY'] = ('projeto-hackaton-sempre-perto')
db.init_app(app)

from views import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)