from init import db

class Playlist(db.Model):
    """Model for Playlist."""
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    name = db.Column(db.String, nullable=False)  # Playlist Name
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='playlists')
    songs = db.relationship('PlaylistSong', back_populates='playlist', cascade='all')  # Reference PlaylistSong directly