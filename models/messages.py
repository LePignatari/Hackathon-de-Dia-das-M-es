from db import db

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

    def to_dict(self):
        return{'id':self.id, 'content':self.content, 'sender_id':self.sender_id, 'receiver_id':self.receiver_id}
    
    