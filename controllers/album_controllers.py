from flask import Blueprint, request
from init import db
from models.album import Album
from schemas.album_schema import AlbumSchema
from flask_jwt_extended import jwt_required
from sqlalchemy import select

albums_bp = Blueprint("albums", __name__, url_prefix="/albums")

@albums_bp.route("/", methods=["POST"])
def create_album():
    """Create a new album."""
    body_data = request.get_json()
    album = Album(title=body_data.get("title"))
    db.session.add(album)
    db.session.commit()
    return AlbumSchema().dump(album), 201

@albums_bp.route("/", methods=["GET"])
def get_all_albums():
    """Get all albums."""
    albums = Album.query.all()
    return AlbumSchema(many=True).dump(albums)

@albums_bp.route("/<int:album_id>", methods=["GET"])
def get_album(album_id):
    """Get a specific album."""
    album = Album.query.get_or_404(album_id)
    return AlbumSchema().dump(album)

@albums_bp.route("/<int:album_id>", methods=["DELETE"])
@jwt_required()
# Delete a album by its ID
def delete_album(album_id):
    stmt = select(Album).filter_by(id=album_id)
    album = db.session.scalar(stmt)
    
    if album:
        db.session.delete(album) # Delete the album from the session
        db.session.commit() #Commit to the database
        return {"message": f"Artist {album.title} deleted successfully!"}
    
    return {"error": "album not found"}, 404 # Handle where album is not found