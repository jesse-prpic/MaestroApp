from flask import Blueprint, request
from init import db
from models.song import Song
from models.genre import Genre
from flask_jwt_extended import jwt_required
from schemas.song_schema import SongSchema
from sqlalchemy import select
import logging

songs_bp = Blueprint("songs", __name__, url_prefix="/songs")

@songs_bp.route("/", methods=["POST"])
def create_song():
    """Create a new song."""
    body_data = request.get_json()

    # Get genre_id from the request
    genre_id = body_data.get("genre_id")
    genre = Genre.query.get(genre_id)  # Use the model name to avoid conflicts

    if genre is None:
        return {"message": "Genre not found!"}, 404

    song = Song(
        title=body_data.get("title"),
        artist_id=body_data.get("artist_id"),
        genre_id=genre_id,
        album_id=body_data.get("album_id"),
    )
    
    try:
        db.session.add(song)
        db.session.commit()
        return {"message": "Song added successfully", "song": SongSchema().dump(song)}, 201
    except Exception as e:
        logging.error(f"Error creating song: {e}")
        db.session.rollback()
        return {"error": "Failed to create song"}, 400

@songs_bp.route("/", methods=["GET"])
def get_all_songs():
    """Get all songs."""
    songs = Song.query.all()
    return SongSchema(many=True).dump(songs)

@songs_bp.route("/<int:song_id>", methods=["DELETE"])
@jwt_required()
def delete_song(song_id):
    """Delete a song by its ID."""
    stmt = select(Song).filter_by(id=song_id)
    song = db.session.scalar(stmt)
    
    if song:
        try:
            db.session.delete(song)
            db.session.commit()
            return {"message": f"Song {song.title} deleted successfully!"}
        except Exception as e:
            logging.error(f"Error deleting song: {e}")
            db.session.rollback()
            return {"error": "Failed to delete song"}, 400
    
    return {"error": "Song not found"}, 404

@songs_bp.route("/<int:song_id>", methods=["PATCH"])
@jwt_required()
def update_song(song_id):
    body_data = request.get_json()
    song = Song.query.get(song_id)

    if song:
        try:
            song.title = body_data.get("title", song.title)
            song.genre_id = body_data.get("genre_id", song.genre_id)
            song.artist_id = body_data.get("artist_id", song.artist_id)
            song.album_id = body_data.get("album_id", song.album_id)
            db.session.commit()
            return SongSchema().dump(song)
        except Exception as e:
            logging.error(f"Error updating song: {e}")
            db.session.rollback()
            return {"error": "Failed to update song"}, 400

    return {"error": "Song not found"}, 404