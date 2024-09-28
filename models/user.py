from init import db

class User(db.Model):
    """Model representing a User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True) #Primary Key
    name = db.Column(db.String, nullable=False) #User Name
    email = db.Column(db.String, unique=True, nullable=False) #User email(must be unique)
    password = db.Column(db.String, nullable=False) #Hashed password
    is_admin = db.Column(db.Boolean, default=False) # if user is admin
    
    playlists = db.relationship('Playlist', back_populates='user', cascade="all") #Relationship with Playlist and cascade options