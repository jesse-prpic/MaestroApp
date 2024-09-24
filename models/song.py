from init import db

class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    artist = db.relationship('Artist', back_populates='songs')
    genre = db.relationship('Genre', back_populates='songs')
    album = db.relationship('Album', back_populates='songs')

