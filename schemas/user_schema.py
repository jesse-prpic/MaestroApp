from init import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    playlists = fields.List(fields.Nested('PlaylistSchema', only=["id", "name"]))

    class Meta:
        fields = ("id", "name", "email", "playlists")
        ordered = True