from init import db

class Album(db.Model):
    """Model for Album."""
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    title = db.Column(db.String(255), unique=True, nullable=False)  # Album Title
    songs = db.relationship('Song', back_populates='album', cascade="all")  # Relationship with Song and cascade options