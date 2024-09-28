from flask import Blueprint, request, jsonify
from init import db
from models.artist import Artist
from schemas.artist_schema import ArtistSchema
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from utility_functions import auth_as_admin
import logging

# Blueprint for artist-related routes
artists_bp = Blueprint("artists", __name__, url_prefix="/artists")

@artists_bp.route("/", methods=["POST"])
def create_artist():
    """Create a new artist."""
    try:
        body_data = request.get_json()
        if not body_data or not body_data.get("name"):
            return {"error": "Name is required"}, 400

        artist = Artist(name=body_data["name"])
        db.session.add(artist)
        db.session.commit()
        return ArtistSchema().dump(artist), 201
    except Exception as e:
        logging.error(f"Error in create_artist: {str(e)}")
        return jsonify({"error": "Failed to create artist."}), 500

@artists_bp.route("/", methods=["GET"])
def get_all_artists():
    """Get all artists."""
    try:
        artists = Artist.query.all()
        return ArtistSchema(many=True).dump(artists), 200
    except Exception as e:
        logging.error(f"Error in get_all_artists: {str(e)}")
        return jsonify({"error": "Failed to fetch artists."}), 500

@artists_bp.route("/<int:artist_id>", methods=["GET"])
def get_artist(artist_id):
    """Get a specific artist."""
    try:
        artist = Artist.query.get_or_404(artist_id)
        return ArtistSchema().dump(artist), 200
    except Exception as e:
        logging.error(f"Error in get_artist: {str(e)}")
        return jsonify({"error": "Failed to fetch artist."}), 500

@artists_bp.route("/<int:artist_id>", methods=["DELETE"])
@auth_as_admin
@jwt_required()
def delete_artist(artist_id):
    """Delete an artist by its ID."""
    try:
        stmt = select(Artist).filter_by(id=artist_id)
        artist = db.session.scalar(stmt)
        
        if artist:
            db.session.delete(artist)
            db.session.commit()
            return {"message": f"Artist {artist.name} deleted successfully!"}, 200
        
        return {"error": "Artist not found"}, 404
    except Exception as e:
        logging.error(f"Error in delete_artist: {str(e)}")
        return jsonify({"error": "Failed to delete artist."}), 500