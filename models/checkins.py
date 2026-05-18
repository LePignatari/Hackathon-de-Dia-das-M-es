from db import db

class Checkin(db.Model):
    __tablename__ = 'checkin'

    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return{'id':self.id,'emotion':self.emotion,'user_id':self.user_id}
    