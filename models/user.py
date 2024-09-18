from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    playlists = db.relationship('Playlist', back_populates='user')

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User