from init import ma
from marshmallow import fields

class PlaylistSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=["id", "name"])

    class Meta:
        fields = ("id", "name", "user")
        ordered = True