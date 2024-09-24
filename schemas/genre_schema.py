from init import ma
from marshmallow import fields

class GenreSchema(ma.Schema):
    songs = fields.List(fields.Nested('SongSchema', only=["id", "title"]))

    class Meta:
        fields = ("id", "name", "songs")
        ordered = True