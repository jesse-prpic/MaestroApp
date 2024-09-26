from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from sqlalchemy import select
from schemas.playlist_schema import PlaylistSchema
from models.playlist import Playlist

# Create a blueprint for playlist-related routes
playlists_bp = Blueprint("playlists", __name__, url_prefix="/playlists")

@playlists_bp.route("/", methods=["GET"])
@jwt_required()
# Get all playlists for the authenticated user
def get_all_playlists():
    user_id = get_jwt_identity()
    stmt = select(Playlist).filter_by(user_id=user_id)
    playlists = db.session.scalars(stmt).all()
    return PlaylistSchema(many=True).dump(playlists), 200

@playlists_bp.route("/", methods=["POST"])
@jwt_required()
# Create a new playlist for the authenticated user
def create_playlist():
    body_data = request.get_json()
    user_id = get_jwt_identity()
    playlist = Playlist(
        name=body_data.get("name"),
        user_id=user_id
    )
    db.session.add(playlist)
    db.session.commit()
    return PlaylistSchema().dump(playlist), 201

@playlists_bp.route("/<int:playlist_id>", methods=["PATCH"])
@jwt_required()
def update_playlist(playlist_id):
    body_data = request.get_json()
    stmt = select(Playlist).filter_by(id=playlist_id)
    playlist = db.session.scalar(stmt)
    if playlist:
        playlist.name = body_data.get("name", playlist.name)
        db.session.commit()
        return PlaylistSchema().dump(playlist)
    return {"error": "Playlist not found"}, 404

@playlists_bp.route("/<int:playlist_id>", methods=["DELETE"])
@jwt_required()
# Delete a playlist by its ID
def delete_playlist(playlist_id):
    stmt = select(Playlist).filter_by(id=playlist_id)
    playlist = db.session.scalar(stmt)
    
    if playlist:
        db.session.delete(playlist) # Delete the playlist from the session
        db.session.commit() #Commit to the database
        return {"message": f"Playlist {playlist.name} deleted successfully!"}
    
    return {"error": "Playlist not found"}, 404 # Handle where playlist is not found