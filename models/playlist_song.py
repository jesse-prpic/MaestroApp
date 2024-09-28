from init import db

class PlaylistSong(db.Model):
    """Model representing the association between Playlists and Songs."""
    __tablename__ = "playlist_songs"

    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), primary_key=True)

    playlist = db.relationship('Playlist', back_populates='songs') 
    song = db.relationship('Song', back_populates='playlists')
