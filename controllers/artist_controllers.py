from flask import Blueprint, request
from init import db
from models.artist import Artist
from schemas.artist_schema import ArtistSchema
from flask_jwt_extended import jwt_required
from sqlalchemy import select


artists_bp = Blueprint("artists", __name__, url_prefix="/artists")

@artists_bp.route("/", methods=["POST"])
def create_artist():
    """Create a new artist."""
    body_data = request.get_json()
    artist = Artist(name=body_data.get("name"))
    db.session.add(artist)
    db.session.commit()
    return ArtistSchema().dump(artist), 201

@artists_bp.route("/", methods=["GET"])
def get_all_artists():
    """Get all artists."""
    artists = Artist.query.all()
    return ArtistSchema(many=True).dump(artists)

@artists_bp.route("/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    """Get a specific artist."""
    artist = Artist.query.get_or_404(artist_id)
    return ArtistSchema().dump(artist)

@artists_bp.route("/<int:artist_id>", methods=["DELETE"])
@jwt_required()
# Delete a playlist by its ID
def delete_artist(artist_id):
    stmt = select(Artist).filter_by(id=artist_id)
    artist = db.session.scalar(stmt)
    
    if artist:
        db.session.delete(artist) # Delete the artist from the session
        db.session.commit() #Commit to the database
        return {"message": f"Artist {artist.name} deleted successfully!"}
    
    return {"error": "Artist not found"}, 404 # Handle where artist is not found