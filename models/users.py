from db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    fam_code = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {'id':self.id, 'name':self.name, 'email':self.email, 'user_type':self.user_type, 'fam_code':self.fam_code}
    

