from init import ma
from marshmallow import fields

class SongSchema(ma.Schema):
    """Schema for serializing Song data."""
    
    # Nested artist information, serializing only the 'id' and 'name' fields from ArtistSchema
    artist = fields.Nested('ArtistSchema', only=["id", "name"])
    # Nested genre information, serializing only the 'id' and 'name' fields from GenreSchema
    genre = fields.Nested('GenreSchema', only=["id", "name"])
    # Nested album information, serializing only the 'id' and 'title' fields from AlbumSchema
    album = fields.Nested('AlbumSchema', only=["id", "title"])

    class Meta:
        # Fields to include in the serialized output
        fields = ("id", "title", "artist", "genre", "album")
        # Maintain the order of fields as defined
        ordered = True