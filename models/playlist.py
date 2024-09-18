from init import db, ma
from marshmallow import fields

class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='playlists')

class PlaylistSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=["id", "name"])

    class Meta:
        fields = ("id", "name", "user")
        ordered = True