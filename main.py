import os
from flask import Flask
from controllers.cli_controllers import db_commands
from controllers.auth_controllers import auth_bp
from controllers.playlist_controllers import playlists_bp

from init import db, ma, bcrypt, jwt

def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(playlists_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)