from init import db, ma
from marshmallow import fields

class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    songs = db.relationship('Song', back_populates='genre')

class GenreSchema(ma.Schema):
    songs = fields.List(fields.Nested('SongSchema', only=["id", "title"]))

    class Meta:
        fields = ("id", "name", "songs")
        ordered = True