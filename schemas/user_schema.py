from init import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    playlists = fields.List(fields.Nested('PlaylistSchema', only=["id", "name"])) #Nested list of playlists

    class Meta:
        fields = ("id", "name", "email", "playlists") #Fields to Serialize
        ordered = True #Order to be maintained