from flask import Blueprint, request
from init import db
from models.genre import Genre
from schemas.genre_schema import GenreSchema
from flask_jwt_extended import jwt_required

genres_bp = Blueprint("genres", __name__, url_prefix="/genres")

@genres_bp.route("/", methods=["POST"])
@jwt_required()
def create_genre():
    """Create a new genre."""
    body_data = request.get_json()
    genre = Genre(name=body_data.get("name"))
    db.session.add(genre)
    db.session.commit()
    return GenreSchema().dump(genre), 201

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


@genres_bp.route("/<int:genre_id>", methods=["DELETE"])
@jwt_required()
def delete_genre(genre_id):
    """Delete a specific genre."""
    genre = Genre.query.get_or_404(genre_id)
    db.session.delete(genre)
    db.session.commit()
    return {"message": f"Genre '{genre.name}' deleted successfully!"}, 204