from init import db

class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    title = db.Column(db.String, nullable=False)  # Song Title
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)  # Foreign Key to Artist
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)  # Foreign Key to Genre
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))  # Optional foreign key to Album

    artist = db.relationship('Artist', back_populates='songs')  # Relationship with Artist
    genre = db.relationship('Genre', back_populates='songs')  # Relationship with Genre
    album = db.relationship('Album', back_populates='songs')  # Relationship with Album

