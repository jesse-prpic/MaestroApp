from init import db

class Artist(db.Model):
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True) #Primary Key
    name = db.Column(db.String, nullable=False) #Song name
    songs = db.relationship('Song', back_populates='artist') #Relationship with song