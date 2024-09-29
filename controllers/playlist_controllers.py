from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from sqlalchemy import select
from schemas.playlist_schema import PlaylistSchema
from models.playlist import Playlist
from models.song import Song
from schemas.song_schema import SongSchema
from models.playlist_song import PlaylistSong
import logging

playlists_bp = Blueprint("playlists", __name__, url_prefix="/playlists")

@playlists_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_playlists():
    """Get all playlists for the authenticated user."""
    user_id = get_jwt_identity()
    stmt = select(Playlist).filter_by(user_id=user_id)
    playlists = db.session.scalars(stmt).all()
    return PlaylistSchema(many=True).dump(playlists), 200

@playlists_bp.route("/<int:playlist_id>", methods=["GET"])
def get_playlist(playlist_id):
    """Get a specific playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    return PlaylistSchema().dump(playlist)

@playlists_bp.route("/", methods=["POST"])
@jwt_required()
def create_playlist():
    """Create a new playlist for the authenticated user."""
    body_data = request.get_json()
    user_id = get_jwt_identity()
    try:
        playlist = Playlist(
            name=body_data.get("name"),
            user_id=user_id
        )
        db.session.add(playlist)
        db.session.commit()
        return PlaylistSchema().dump(playlist), 201
    except Exception as e:
        logging.error(f"Error creating playlist: {e}")
        db.session.rollback()
        return {"error": "Failed to create playlist"}, 400

@playlists_bp.route("/<int:playlist_id>", methods=["PATCH"])
@jwt_required()
def update_playlist(playlist_id):
    """Update an existing playlist."""
    body_data = request.get_json()
    stmt = select(Playlist).filter_by(id=playlist_id)
    playlist = db.session.scalar(stmt)
    
    if playlist:
        try:
            playlist.name = body_data.get("name", playlist.name)
            db.session.commit()
            return PlaylistSchema().dump(playlist)
        except Exception as e:
            logging.error(f"Error updating playlist: {e}")
            db.session.rollback()
            return {"error": "Failed to update playlist"}, 400
    
    return {"error": "Playlist not found"}, 404

@playlists_bp.route("/<int:playlist_id>", methods=["DELETE"])
@jwt_required()
def delete_playlist(playlist_id):
    """Delete a playlist by its ID."""
    stmt = select(Playlist).filter_by(id=playlist_id)
    playlist = db.session.scalar(stmt)
    
    if playlist:
        try:
            db.session.delete(playlist)
            db.session.commit()
            return {"message": f"Playlist {playlist.name} deleted successfully!"}
        except Exception as e:
            logging.error(f"Error deleting playlist: {e}")
            db.session.rollback()
            return {"error": "Failed to delete playlist"}, 400
    
    return {"error": "Playlist not found"}, 404

@playlists_bp.route("/<int:playlist_id>/songs", methods=["POST"])
@jwt_required()
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist."""
    body_data = request.get_json()
    song_id = body_data.get("song_id")

    try:
        playlist = Playlist.query.get_or_404(playlist_id)
        song = Song.query.get_or_404(song_id)

        # Check if the song is already in the playlist
        existing_entry = db.session.query(PlaylistSong).filter_by(playlist_id=playlist.id, song_id=song.id).first()
        if existing_entry:
            return {"error": "Song already exists in the playlist"}, 400

        # Create a new PlaylistSong association
        playlist_song = PlaylistSong(playlist_id=playlist.id, song_id=song.id)
        db.session.add(playlist_song)
        db.session.commit()
        return {"message": "Song added to playlist"}, 201
    except Exception as e:
        logging.error(f"Error adding song to playlist: {e}")
        db.session.rollback()
        return {"error": "Failed to add song to playlist"}, 400

@playlists_bp.route("/<int:playlist_id>/songs", methods=["GET"])
@jwt_required()
def get_songs_in_playlist(playlist_id):
    """Get all songs in a specific playlist."""
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return {'error': 'Playlist not found'}, 404

    songs = db.session.query(Song).join(PlaylistSong).filter(PlaylistSong.playlist_id == playlist_id).all()
    
    return [{'id': song.id, 'title': song.title, 'artist_id': song.artist_id} for song in songs], 200

@playlists_bp.route("/<int:playlist_id>/songs/<int:song_id>", methods=["DELETE"])
@jwt_required()
def remove_song_from_playlist(playlist_id, song_id):
    """Remove a song from a playlist."""
    try:
        playlist = Playlist.query.get_or_404(playlist_id)
        song = Song.query.get_or_404(song_id)

        if song not in playlist.songs:
            return {"error": "Song not found in the playlist"}, 404

        playlist.songs.remove(song)
        db.session.commit()
        return {"message": "Song removed from playlist"}, 204
    except Exception as e:
        logging.error(f"Error removing song from playlist: {e}")
        db.session.rollback()
        return {"error": "Failed to remove song from playlist"}, 400