from init import db
from models.playlist_song import PlaylistSong

class Playlist(db.Model):
    """Model representing a Playlist."""
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='playlists')
    songs = db.relationship('PlaylistSong', back_populates='playlist', lazy='dynamic')  # Ensure it's a string reference