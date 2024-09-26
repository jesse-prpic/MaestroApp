from flask import Blueprint, request
from init import db
from models.song import Song
from schemas.song_schema import SongSchema

songs_bp = Blueprint("songs", __name__, url_prefix="/songs")

@songs_bp.route("/", methods=["POST"])
def create_song():
    """Create a new song."""
    body_data = request.get_json()
    song = Song(
        title=body_data.get("title"),
        artist_id=body_data.get("artist_id"),
        genre_id=body_data.get("genre_id"),
        album_id=body_data.get("album_id"),
    )
    db.session.add(song)
    db.session.commit()
    return SongSchema().dump(song), 201

@songs_bp.route("/", methods=["GET"])
def get_all_songs():
    """Get all songs."""
    songs = Song.query.all()
    return SongSchema(many=True).dump(songs)

@songs_bp.route("/<int:song_id>", methods=["GET"])
def get_song(song_id):
    """Get a specific song."""
    song = Song.query.get_or_404(song_id)
    return SongSchema().dump(song)