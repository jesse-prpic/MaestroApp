from flask import Blueprint, request, jsonify
from init import db
from models.song import Song
from schemas.song_schema import SongSchema
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from utility_functions import auth_as_admin
import logging

# Blueprint for song-related routes
songs_bp = Blueprint("songs", __name__, url_prefix="/songs")

@songs_bp.route("/", methods=["POST"])
def create_song():
    """Create a new song."""
    try:
        body_data = request.get_json()
        if not body_data or not body_data.get("title"):
            return {"error": "Title is required"}, 400

        song = Song(title=body_data["title"], artist_id=body_data.get("artist_id"))
        db.session.add(song)
        db.session.commit()
        return SongSchema().dump(song), 201
    except Exception as e:
        logging.error(f"Error in create_song: {str(e)}")
        return jsonify({"error": "Failed to create song."}), 500

@songs_bp.route("/", methods=["GET"])
def get_all_songs():
    """Get all songs."""
    try:
        songs = Song.query.all()
        return SongSchema(many=True).dump(songs), 200
    except Exception as e:
        logging.error(f"Error in get_all_songs: {str(e)}")
        return jsonify({"error": "Failed to fetch songs."}), 500

@songs_bp.route("/<int:song_id>", methods=["GET"])
def get_song(song_id):
    """Get a specific song."""
    try:
        song = Song.query.get_or_404(song_id)
        return SongSchema().dump(song), 200
    except Exception as e:
        logging.error(f"Error in get_song: {str(e)}")
        return jsonify({"error": "Failed to fetch song."}), 500

@songs_bp.route("/<int:song_id>", methods=["DELETE"])
@auth_as_admin
@jwt_required()
def delete_song(song_id):
    """Delete a song by its ID."""
    try:
        stmt = select(Song).filter_by(id=song_id)
        song = db.session.scalar(stmt)

        if song:
            db.session.delete(song)
            db.session.commit()
            return {"message": f"Song {song.title} deleted successfully!"}, 200

        return {"error": "Song not found"}, 404
    except Exception as e:
        logging.error(f"Error in delete_song: {str(e)}")
        return jsonify({"error": "Failed to delete song."}), 500