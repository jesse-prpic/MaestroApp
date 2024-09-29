from flask import Blueprint, request
from init import db
from models.artist import Artist
from schemas.artist_schema import ArtistSchema
from flask_jwt_extended import jwt_required
from sqlalchemy import select
import logging

artists_bp = Blueprint("artists", __name__, url_prefix="/artists")

@artists_bp.route("/", methods=["POST"])
def create_artist():
    """Create a new artist.

    Returns:
        dict: Response containing the created artist or an error message.
    """
    body_data = request.get_json()

    if not body_data or 'name' not in body_data:
        return {"error": "Name is required."}, 400

    try:
        artist = Artist(name=body_data["name"])
        db.session.add(artist)
        db.session.commit()
        return ArtistSchema().dump(artist), 201
    except Exception as e:
        logging.error(f"Error creating artist: {e}")
        return {"error": "Failed to create artist."}, 500

@artists_bp.route("/", methods=["GET"])
def get_all_artists():
    """Get all artists.

    Returns:
        dict: Response containing all artists or an error message.
    """
    try:
        artists = Artist.query.all()
        return ArtistSchema(many=True).dump(artists)
    except Exception as e:
        logging.error(f"Error fetching artists: {e}")
        return {"error": "Failed to fetch artists."}, 500

@artists_bp.route("/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    """Get a specific artist by ID.

    Args:
        artist_id (int): The ID of the artist to retrieve.

    Returns:
        dict: Response containing the artist or an error message.
    """
    try:
        artist = Artist.query.get_or_404(artist_id)
        return ArtistSchema().dump(artist)
    except Exception as e:
        logging.error(f"Error retrieving artist {artist_id}: {e}")
        return {"error": "An error occurred while retrieving the artist."}, 500

@artists_bp.route("/<int:artist_id>", methods=["DELETE"])
@jwt_required()
def delete_artist(artist_id):
    """Delete an artist by its ID.

    Args:
        artist_id (int): The ID of the artist to delete.

    Returns:
        dict: Response containing a success message or an error message.
    """
    try:
        stmt = select(Artist).filter_by(id=artist_id)
        artist = db.session.scalar(stmt)

        if artist:
            db.session.delete(artist)
            db.session.commit()
            return {"message": f"Artist {artist.name} deleted successfully!"}
        
        return {"error": "Artist not found."}, 404
    except Exception as e:
        logging.error(f"Error deleting artist: {e}")
        return {"error": "Failed to delete artist."}, 500
    
@artists_bp.route("/<int:artist_id>", methods=["PATCH"])
@jwt_required()
def update_artist(artist_id):
    body_data = request.get_json()
    artist = Artist.query.get(artist_id)

    if artist:
        try:
            artist.name = body_data.get("name", artist.name)
            db.session.commit()
            return ArtistSchema().dump(artist)
        except Exception as e:
            logging.error(f"Error updating artist: {e}")
            db.session.rollback()
            return {"error": "Failed to update artist"}, 400

    return {"error": "Artist not found"}, 404