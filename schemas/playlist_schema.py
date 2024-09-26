from init import ma
from marshmallow import fields

class PlaylistSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=["id", "name"]) #Nested user information

    class Meta:
        fields = ("id", "name", "user") #Fields to serialize
        ordered = True #Order to be maintained