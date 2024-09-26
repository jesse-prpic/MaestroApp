from flask import Blueprint, request
from init import db
from models.genre import Genre
from schemas.genre_schema import GenreSchema

genres_bp = Blueprint("genres", __name__, url_prefix="/genres")

@genres_bp.route("/", methods=["GET"])
def get_all_genres():
    """Get all genres."""
    genres = Genre.query.all()
    return GenreSchema(many=True).dump(genres)

@genres_bp.route("/<int:genre_id>", methods=["GET"])
def get_genre(genre_id):
    """Get a specific genre."""
    genre = Genre.query.get_or_404(genre_id)
    return GenreSchema().dump(genre)