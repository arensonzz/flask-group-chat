import os
from flask import Flask


def create_app(test_config=None):
    """Create and return Flask instance"""
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # Set config values
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flask_group_chat.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize app with database commands
    from . import db
    db.init_app(app)

    # Register blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    # A route to test Flask connection
    @app.route('/test')
    def test():
        return "Server is working.", 200

    return app
