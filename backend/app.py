from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from config import Config
from models import db

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    CORS(app)
    migrate = Migrate(app, db)

    # Register blueprints
    from routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/api')

    # Create database tables
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return {'message': 'Todo List API is running', 'version': '1.0.0'}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
