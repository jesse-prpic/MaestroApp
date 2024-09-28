import os
from flask import Flask, jsonify
from controllers.auth_controllers import auth_bp
from controllers.cli_controllers import db_commands
from controllers.playlist_controllers import playlists_bp
from controllers.artist_controllers import artists_bp
from controllers.album_controllers import albums_bp
from controllers.song_controllers import songs_bp
from controllers.genre_controllers import genres_bp
from werkzeug.exceptions import BadRequest  # Import for raising BadRequest


from init import db, ma, bcrypt, jwt

# Create a flask app
def create_app():
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

# Error handling for HTTP errors
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error", "message": "Something went wrong"}), 500

    return app

# Create and run the app
if __name__ == "__main__":
    app = create_app() 
    app.run(host='0.0.0.0', port=5000)
