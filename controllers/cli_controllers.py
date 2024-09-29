from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.artist import Artist
from models.playlist import Playlist
from models.song import Song
from models.album import Album
from models.genre import Genre

# Create a blueprint for database CLI commands
db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped!")

@db_commands.cli.command("seed")
def seed_tables():
    # Create sample users
    user_attribute = [
        User(name="Jesse", email="jesse@admin.com", password=bcrypt.generate_password_hash("password").decode("utf-8"), is_admin=True),
        User(name="Alice", email="alice@admin.com", password=bcrypt.generate_password_hash("password").decode("utf-8"), is_admin=False),
    ]
    db.session.add_all(user_attribute)
    
    # Create sample playlist
    playlist_attibute = [
        Playlist(name="Jesse's Playlist", user_id=1),
        Playlist(name="Alice's Playlist", user_id=2),
    ]
    db.session.add_all(playlist_attibute)

    # Create sample artists
    artist_attribute = [
        Artist(name="Taylor Swift"),
        Artist(name="Hilary Duff"),
    ]
    db.session.add_all(artist_attribute)

    # Create sample genres
    genre_attribute = [
        Genre(name="Rock"),
        Genre(name="Pop"),
        Genre(name="Hip Hop"),
        Genre(name="Alternative"),
        Genre(name="Country"),
        Genre(name="Classical"),
    ]
    db.session.add_all(genre_attribute)

    # Create sample albums
    album_attribute = [
        Album(title="Reputation (Taylors Version)"),
        Album(title="Metamorphosis"),
    ]
    db.session.add_all(album_attribute)

    # Create sample songs
    song_attribute = [
        Song(title="Don't Blame Me", artist_id=1, genre_id=1, album_id=1),
        Song(title="Who's That Girl", artist_id=2, genre_id=2, album_id=2),
    ]
    db.session.add_all(song_attribute)

    # Commit all changes to the database
    db.session.commit()
    print("Tables seeded!")