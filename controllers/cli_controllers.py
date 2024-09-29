from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.artist import Artist
from models.playlist import Playlist
from models.song import Song
from models.album import Album
from models.genre import Genre
import logging

# Create a blueprint for database CLI commands
db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    """Create all database tables."""
    try:
        db.create_all()
        print("Tables created!")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")

@db_commands.cli.command("drop")
def drop_tables():
    """Drop all database tables."""
    try:
        db.drop_all()
        print("Tables dropped!")
    except Exception as e:
        logging.error(f"Error dropping tables: {e}")

@db_commands.cli.command("seed")
def seed_tables():
    """Seed the database with initial data."""
    try:
        # Sample data creation
        users = [
            User(name="Jesse", email="jesse@admin.com", password=bcrypt.generate_password_hash("password").decode("utf-8"), is_admin=True),
            User(name="Alice", email="alice@admin.com", password=bcrypt.generate_password_hash("password").decode("utf-8"), is_admin=False),
        ]
        db.session.add_all(users)

        playlists = [
            Playlist(name="Jesse's Playlist", user_id=1),
            Playlist(name="Alice's Playlist", user_id=2),
        ]
        db.session.add_all(playlists)

        artists = [
            Artist(name="Taylor Swift"),
            Artist(name="Hilary Duff"),
        ]
        db.session.add_all(artists)

        genres = [
            Genre(name="Rock"),
            Genre(name="Pop"),
            Genre(name="Hip Hop"),
            Genre(name="Alternative"),
            Genre(name="Country"),
            Genre(name="Classical"),
        ]
        db.session.add_all(genres)

        albums = [
            Album(title="Reputation (Taylor's Version)"),
            Album(title="Metamorphosis"),
        ]
        db.session.add_all(albums)

        songs = [
            Song(title="Don't Blame Me", artist_id=1, genre_id=1, album_id=1),
            Song(title="Who's That Girl", artist_id=2, genre_id=2, album_id=2),
        ]
        db.session.add_all(songs)

        # Commit all changes to the database
        db.session.commit()
        print("Tables seeded!")
    except Exception as e:
        logging.error(f"Error seeding database: {e}")
        db.session.rollback()