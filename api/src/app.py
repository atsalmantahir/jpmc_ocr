from flask import Flask
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from models.user_model import db, User

# Register Blueprints (controllers)
from controllers.documents_controller import documents_bp
from controllers.auth_controller import auth_bp
from controllers.user_controller import user_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

# Enable CORS for all routes
CORS(app)

# Set up logging
def setup_logging():
    # Create a log file with rotation
    log_handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=3)  # Rotate after 1MB, keep 3 backups
    log_handler.setLevel(logging.INFO)

    # Create a logging format
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_handler.setFormatter(log_format)

    # Add handler to the app's logger
    app.logger.addHandler(log_handler)

    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    app.logger.addHandler(console_handler)

# Setup logging
setup_logging()

# Register Blueprints

app.register_blueprint(documents_bp, url_prefix='/api/documents')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/user')

# User loader for flask-login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Setup Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # URL for Swagger JSON
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Document Demo API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Initialize the DB
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)