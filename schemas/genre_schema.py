from init import ma
from marshmallow import fields

class GenreSchema(ma.Schema):
    """Schema for serializing Genre data."""
    
    # Nested list of songs, serializing only the 'id' and 'title' fields from SongSchema
    songs = fields.List(fields.Nested('SongSchema', only=["id", "title"]))

    class Meta:
        # Fields to include in the serialized output
        fields = ("id", "name", "songs")
        # Maintain the order of fields as defined
        ordered = True