from init import ma
from marshmallow import fields

class SongSchema(ma.Schema):
    artist = fields.Nested('ArtistSchema', only=["id", "name"])
    genre = fields.Nested('GenreSchema', only=["id", "name"])
    album = fields.Nested('AlbumSchema', only=["id", "title"])

    class Meta:
        fields = ("id", "title", "artist", "genre", "album")
        ordered = True