from init import ma
from marshmallow import fields

class SongSchema(ma.Schema):
    artist = fields.Nested('ArtistSchema', only=["id", "name"]) #Nested artist information
    genre = fields.Nested('GenreSchema', only=["id", "name"]) #Nested genre information
    album = fields.Nested('AlbumSchema', only=["id", "title"]) #Nested album information

    class Meta:
        fields = ("id", "title", "artist", "genre", "album") #Fields to serialize
        ordered = True #Order to be maintained