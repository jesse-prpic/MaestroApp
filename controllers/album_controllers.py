from flask import Blueprint, request
from init import db
from models.album import Album
from schemas.album_schema import AlbumSchema

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