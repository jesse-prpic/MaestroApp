from init import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    """Schema for serializing User data."""
    
    # Nested list of playlists, serializing only the 'id' and 'name' fields from PlaylistSchema
    playlists = fields.List(fields.Nested('PlaylistSchema', only=["id", "name"]))

    class Meta:
        # Fields to include in the serialized output
        fields = ("id", "name", "email", "playlists")
        # Maintain the order of fields as defined
        ordered = True