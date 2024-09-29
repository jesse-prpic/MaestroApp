from init import db

class Artist(db.Model):
    """Model for Artist."""
    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    name = db.Column(db.String(255), unique=True, nullable=False)  # Artist Name
    songs = db.relationship('Song', back_populates='artist', cascade="all")  # Relationship with Song and cascade options