import os
from flask import Flask, jsonify
from controllers.auth_controllers import auth_bp
from controllers.cli_controllers import db_commands
from controllers.playlist_controllers import playlists_bp
from controllers.artist_controllers import artists_bp
from controllers.album_controllers import albums_bp
from controllers.song_controllers import songs_bp
from controllers.genre_controllers import genres_bp

from init import db, ma, bcrypt, jwt

# Create a flask app
def create_app():
    
    """Create and configure the Flask app.

    Returns:
        Flask: Configured app instance.
    """

    app = Flask(__name__)
    app.json.sort_keys = False

    # set configurations from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # initialise the extensions within the app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Regiester blueprints for different routes
    app.register_blueprint(auth_bp) #Authentication routes
    app.register_blueprint(db_commands) # CLI commands for DB management
    app.register_blueprint(playlists_bp) # PLaylist-related routes
    app.register_blueprint(artists_bp) #artist- related routes
    app.register_blueprint(albums_bp) #album-related routes
    app.register_blueprint(songs_bp) #song-related routes
    app.register_blueprint(genres_bp) #genre-related routes

    return app

# Create and run the app
if __name__ == "__main__":
    app = create_app() 
    app.run(host='0.0.0.0', port=5000)
