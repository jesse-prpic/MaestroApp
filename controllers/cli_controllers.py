from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.artist import Artist
from models.playlist import Playlist
from models.song import Song
from models.album import Album
from models.genre import Genre

# Blueprint for database CLI commands
db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    """Create all database tables."""
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_tables():
    """Drop all database tables."""
    db.drop_all()
    print("Tables dropped!")

@db_commands.cli.command("seed")
def seed_db():
    """Seed the database with initial data."""
    print("Seeding database...")

    # Create sample users
    user1 = User(name="Admin User", email="admin@example.com", password=bcrypt.generate_password_hash("password").decode("utf-8"))
    user2 = User(name="Regular User", email="user@example.com", password=bcrypt.generate_password_hash("password").decode("utf-8"))
    
    # Create sample artists
    artist1 = Artist(name="Artist 1")
    artist2 = Artist(name="Artist 2")
    
    # Create sample genres
    genre1 = Genre(name="Pop")
    genre2 = Genre(name="Rock")
    
    # Create sample albums
    album1 = Album(title="Album 1")
    album2 = Album(title="Album 2")
    
    # Create sample playlists
    playlist1 = Playlist(name="Playlist 1")
    playlist2 = Playlist(name="Playlist 2")
    
    # Add all data to the session
    db.session.add_all([user1, user2, artist1, artist2, genre1, genre2, album1, album2, playlist1, playlist2])
    db.session.commit()
    
    print("Database seeded!")