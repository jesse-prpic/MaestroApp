from init import ma
from marshmallow import fields

class AlbumSchema(ma.Schema):
    songs = fields.List(fields.Nested('SongSchema', only=["id", "title"])) # Nested list of songs

    class Meta:
        fields = ("id", "title", "songs") # Fields to serialize
        ordered = True #Order to be maintained