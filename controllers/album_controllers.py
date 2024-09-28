from flask import Blueprint, request, jsonify
from init import db
from models.album import Album
from schemas.album_schema import AlbumSchema
from flask_jwt_extended import jwt_required
from sqlalchemy import select
from utility_functions import auth_as_admin
import logging

# Blueprint for album-related routes
albums_bp = Blueprint("albums", __name__, url_prefix="/albums")

@albums_bp.route("/", methods=["POST"])
def create_album():
    """Create a new album."""
    try:
        body_data = request.get_json()
        if not body_data or not body_data.get("title"):
            return {"error": "Title is required"}, 400
        
        album = Album(title=body_data["title"])
        db.session.add(album)
        db.session.commit()
        return AlbumSchema().dump(album), 201
    except Exception as e:
        logging.error(f"Error in create_album: {str(e)}")
        return jsonify({"error": "Failed to create album."}), 500

@albums_bp.route("/", methods=["GET"])
def get_all_albums():
    """Get all albums."""
    try:
        albums = Album.query.all()
        return AlbumSchema(many=True).dump(albums), 200
    except Exception as e:
        logging.error(f"Error in get_all_albums: {str(e)}")
        return jsonify({"error": "Failed to fetch albums."}), 500

@albums_bp.route("/<int:album_id>", methods=["GET"])
def get_album(album_id):
    """Get a specific album."""
    try:
        album = Album.query.get_or_404(album_id)
        return AlbumSchema().dump(album), 200
    except Exception as e:
        logging.error(f"Error in get_album: {str(e)}")
        return jsonify({"error": "Failed to fetch album."}), 500

@albums_bp.route("/<int:album_id>", methods=["DELETE"])
@auth_as_admin
@jwt_required()
def delete_album(album_id):
    """Delete an album by its ID."""
    try:
        stmt = select(Album).filter_by(id=album_id)
        album = db.session.scalar(stmt)
        
        if album:
            db.session.delete(album)
            db.session.commit()
            return {"message": f"Album {album.title} deleted successfully!"}, 200
        
        return {"error": "Album not found"}, 404
    except Exception as e:
        logging.error(f"Error in delete_album: {str(e)}")
        return jsonify({"error": "Failed to delete album."}), 500