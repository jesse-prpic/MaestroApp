from init import db

class Song(db.Model):
    """Model for Song."""
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    title = db.Column(db.String, nullable=False)  # Song Title
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    artist = db.relationship('Artist', back_populates='songs')
    genre = db.relationship('Genre', back_populates='songs')
    album = db.relationship('Album', back_populates='songs')
    playlists = db.relationship('PlaylistSong', back_populates='song')  # Reference PlaylistSong directly