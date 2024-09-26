from init import ma
from marshmallow import fields

class GenreSchema(ma.Schema):
    songs = fields.List(fields.Nested('SongSchema', only=["id", "title"])) # Nested list of songs

    class Meta:
        fields = ("id", "name", "songs") # Fields to serialize
        ordered = True # Order to be maintained