from init import db

class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True) #Primary Key
    name = db.Column(db.String, nullable=False) #Playlist Name
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) #Foreign Key to User

    user = db.relationship('User', back_populates='playlists') #Relationship with user
