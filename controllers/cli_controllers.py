from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.playlist import Playlist

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
    # Create a sample user and playlist
    user = User(
        name="Admin",
        email="admin@example.com",
        password=bcrypt.generate_password_hash("password").decode("utf-8"),
    )
    db.session.add(user)
    
    playlist = Playlist(name="My Favorite Songs", user_id=1)
    db.session.add(playlist)
    
    db.session.commit()
    print("Tables seeded!")