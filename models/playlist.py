from init import db

class Playlist(db.Model):
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='playlists')
    songs = db.relationship('PlaylistSong', back_populates='playlist', cascade='all')  # Reference PlaylistSong directly