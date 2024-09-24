from init import ma
from marshmallow import fields

class AlbumSchema(ma.Schema):
    songs = fields.List(fields.Nested('SongSchema', only=["id", "title"]))

    class Meta:
        fields = ("id", "title", "songs")
        ordered = True