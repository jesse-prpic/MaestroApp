from init import db

class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    songs = db.relationship('Song', back_populates='album')