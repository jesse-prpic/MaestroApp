from init import db

class Genre(db.Model):
    __tablename__ = "genres"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    songs = db.relationship('Song', back_populates='genre')