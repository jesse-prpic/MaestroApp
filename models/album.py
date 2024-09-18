from init import db, ma
from marshmallow import fields

class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    songs = db.relationship('Song', back_populates='album')

class AlbumSchema(ma.Schema):
    songs = fields.List(fields.Nested('SongSchema', only=["id", "title"]))

    class Meta:
        fields = ("id", "title", "songs")
        ordered = True