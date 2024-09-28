from init import db

class Genre(db.Model):
    """Model representing on Genre"""
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True) # Primary key
    name = db.Column(db.String(255), unique=True, nullable=False) # Genre Type
    songs = db.relationship('Song', back_populates='genre', cascade="all") #Relationship with Playlist and cascade options