from flask import Blueprint, request, jsonify
from init import db
from models.genre import Genre
from schemas.genre_schema import GenreSchema
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from utility_functions import auth_as_admin
import logging

# Blueprint for genre-related routes
genres_bp = Blueprint("genres", __name__, url_prefix="/genres")

@genres_bp.route("/", methods=["POST"])
def create_genre():
    """Create a new genre."""
    try:
        body_data = request.get_json()
        if not body_data or not body_data.get("name"):
            return {"error": "Name is required"}, 400

        genre = Genre(name=body_data["name"])
        db.session.add(genre)
        db.session.commit()
        return GenreSchema().dump(genre), 201
    except Exception as e:
        logging.error(f"Error in create_genre: {str(e)}")
        return jsonify({"error": "Failed to create genre."}), 500

@genres_bp.route("/", methods=["GET"])
def get_all_genres():
    """Get all genres."""
    try:
        genres = Genre.query.all()
        return GenreSchema(many=True).dump(genres), 200
    except Exception as e:
        logging.error(f"Error in get_all_genres: {str(e)}")
        return jsonify({"error": "Failed to fetch genres."}), 500

@genres_bp.route("/<int:genre_id>", methods=["GET"])
def get_genre(genre_id):
    """Get a specific genre."""
    try:
        genre = Genre.query.get_or_404(genre_id)
        return GenreSchema().dump(genre), 200
    except Exception as e:
        logging.error(f"Error in get_genre: {str(e)}")
        return jsonify({"error": "Failed to fetch genre."}), 500

@genres_bp.route("/<int:genre_id>", methods=["DELETE"])
@auth_as_admin
@jwt_required()
def delete_genre(genre_id):
    """Delete a genre by its ID."""
    try:
        stmt = select(Genre).filter_by(id=genre_id)
        genre = db.session.scalar(stmt)

        if genre:
            db.session.delete(genre)
            db.session.commit()
            return {"message": f"Genre {genre.name} deleted successfully!"}, 200

        return {"error": "Genre not found"}, 404
    except Exception as e:
        logging.error(f"Error in delete_genre: {str(e)}")
        return jsonify({"error": "Failed to delete genre."}), 500