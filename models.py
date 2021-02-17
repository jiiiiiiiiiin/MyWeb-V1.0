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
        return '<user %r>' % self.username


class Apps(db.Model):
    __tablename__ = "apps"
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(80), nullable=True)
    app_url = db.Column(db.String(80), nullable=True)
    app_status = db.Column(db.String(80), nullable=True)
    app_authority = db.Column(db.Integer, nullable=True)
    app_id = db.Column(db.String(80), nullable=True)  # 注册完成后 这个值不允许修改了

    def __repr__(self):
        return '<AppName %r>' % self.app_name
