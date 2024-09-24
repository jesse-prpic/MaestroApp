from init import ma
from marshmallow import fields

class ArtistSchema(ma.Schema):
    songs = fields.List(fields.Nested('SongSchema', only=["id", "title"]))

    class Meta:
        fields = ("id", "name", "songs")
        ordered = True