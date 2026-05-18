from flask import Flask
from db import db
from models.users import User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
app.config['SECRET_KEY'] = 'projeto-hackathon-sempre-perto'

db.init_app(app)

from views import *

with app.app_context():
        db.create_all()

if __name__ == "__main__":
    app.run(debug=True)