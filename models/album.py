from init import db

class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True) # Primary Key
    title = db.Column(db.String, nullable=False) # Album Title
    songs = db.relationship('Song', back_populates='album') #Relationship with Song