from flask import Blueprint, request
from init import db
from models.album import Album
from schemas.album_schema import AlbumSchema
from flask_jwt_extended import jwt_required
from sqlalchemy import select
import logging

albums_bp = Blueprint("albums", __name__, url_prefix="/albums")

@albums_bp.route("/", methods=["POST"])
def create_album():
    """Create a new album."""

    body_data = request.get_json()

    if not body_data or 'title' not in body_data:
        return {"error": "Title is required."}, 400

    try:
        album = Album(title=body_data["title"])
        db.session.add(album)
        db.session.commit()
        return AlbumSchema().dump(album), 201
    except Exception as e:
        logging.error(f"Error creating album: {e}")
        return {"error": "Failed to create album."}, 500

@albums_bp.route("/", methods=["GET"])
def get_all_albums():
    """Get all albums. """
    try:
        albums = Album.query.all()
        return AlbumSchema(many=True).dump(albums)
    except Exception as e:
        logging.error(f"Error fetching albums: {e}")
        return {"error": "Failed to fetch albums."}, 500

@albums_bp.route("/<int:album_id>", methods=["GET"])
def get_album(album_id):
    """Get a specific album by its ID."""
    try:
        album = Album.query.get_or_404(album_id)
        return AlbumSchema().dump(album)
    except Exception as e:
        logging.error(f"Error retrieving album {album_id}: {e}")
        return {"error": "An error occurred while retrieving the album."}, 500

@albums_bp.route("/<int:album_id>", methods=["DELETE"])
@jwt_required()
def delete_album(album_id):
    """Delete an album by its ID. """
    try:
        stmt = select(Album).filter_by(id=album_id)
        album = db.session.scalar(stmt)

        if album:
            db.session.delete(album)
            db.session.commit()
            return {"message": f"Album {album.title} deleted successfully!"}
        
        return {"error": "Album not found."}, 404
    except Exception as e:
        logging.error(f"Error deleting album: {e}")
        return {"error": "Failed to delete album."}, 500

@albums_bp.route("/<int:album_id>", methods=["PATCH"])
@jwt_required()
def update_album(album_id):
    body_data = request.get_json()
    album = Album.query.get(album_id)

    if album:
        try:
            album.title = body_data.get("title", album.title)
            db.session.commit()
            return AlbumSchema().dump(album)
        except Exception as e:
            logging.error(f"Error updating album: {e}")
            db.session.rollback()
            return {"error": "Failed to update album"}, 400

    return {"error": "Album not found"}, 404