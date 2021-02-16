from datetime import datetime
from exts import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=False)
    authority = db.Column(db.Integer, nullable=True)
    headPhoto = db.Column(db.String(80), nullable=True)
    createTime = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.username
