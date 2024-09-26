from init import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True) #Primary Key
    name = db.Column(db.String, nullable=False) #User Name
    email = db.Column(db.String, unique=True, nullable=False) #User email(must be unique)
    password = db.Column(db.String, nullable=False) #Hashed password
    
    playlists = db.relationship('Playlist', back_populates='user') #Relationship with Playlist