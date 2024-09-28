from flask import Blueprint, request, jsonify
from init import db
from models.playlist import Playlist
from schemas.playlist_schema import PlaylistSchema
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from utility_functions import auth_as_admin
import logging

# Blueprint for playlist-related routes
playlists_bp = Blueprint("playlists", __name__, url_prefix="/playlists")

@playlists_bp.route("/", methods=["POST"])
def create_playlist():
    """Create a new playlist."""
    try:
        body_data = request.get_json()
        if not body_data or not body_data.get("name"):
            return {"error": "Name is required"}, 400

        playlist = Playlist(name=body_data["name"])
        db.session.add(playlist)
        db.session.commit()
        return PlaylistSchema().dump(playlist), 201
    except Exception as e:
        logging.error(f"Error in create_playlist: {str(e)}")
        return jsonify({"error": "Failed to create playlist."}), 500

@playlists_bp.route("/", methods=["GET"])
def get_all_playlists():
    """Get all playlists."""
    try:
        playlists = Playlist.query.all()
        return PlaylistSchema(many=True).dump(playlists), 200
    except Exception as e:
        logging.error(f"Error in get_all_playlists: {str(e)}")
        return jsonify({"error": "Failed to fetch playlists."}), 500

@playlists_bp.route("/<int:playlist_id>", methods=["GET"])
def get_playlist(playlist_id):
    """Get a specific playlist."""
    try:
        playlist = Playlist.query.get_or_404(playlist_id)
        return PlaylistSchema().dump(playlist), 200
    except Exception as e:
        logging.error(f"Error in get_playlist: {str(e)}")
        return jsonify({"error": "Failed to fetch playlist."}), 500

@playlists_bp.route("/<int:playlist_id>", methods=["DELETE"])
@auth_as_admin
@jwt_required()
def delete_playlist(playlist_id):
    """Delete a playlist by its ID."""
    try:
        stmt = select(Playlist).filter_by(id=playlist_id)
        playlist = db.session.scalar(stmt)

        if playlist:
            db.session.delete(playlist)
            db.session.commit()
            return {"message": f"Playlist {playlist.name} deleted successfully!"}, 200

        return {"error": "Playlist not found"}, 404
    except Exception as e:
        logging.error(f"Error in delete_playlist: {str(e)}")
        return jsonify({"error": "Failed to delete playlist."}), 500