from init import ma
from marshmallow import fields

class PlaylistSchema(ma.Schema):
    """Schema for serializing Playlist data."""
    
    # Nested user information, serializing only the 'id' and 'name' fields from UserSchema
    user = fields.Nested('UserSchema', only=["id", "name"])

    class Meta:
        # Fields to include in the serialized output
        fields = ("id", "name", "user")
        # Maintain the order of fields as defined
        ordered = True