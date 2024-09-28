from init import db


class Artist(db.Model):
    """Model representing on Artist"""
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True) #Primary Key
    name = db.Column(db.String(255), unique=True, nullable=False) #Song name
    songs = db.relationship('Song', back_populates='artist', cascade="all") #Relationship with Playlist and cascade options