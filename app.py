"""Backend Showroom - API Flask Modular"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import jwt
from config import Config
from flasgger import Swagger

# Load environment variables from the .env file
load_dotenv()

# Inisialisasi Flask
app = Flask(__name__)
app.config.from_object(Config)

# Middleware
CORS(app)
Swagger(app)
jwt.init_app(app)

# Register Blueprints
from api.auth.endpoints import auth_endpoints
from api.users.endpoints import users_endpoints
from api.vehicles.endpoints import vehicles_endpoints
from api.bookings.endpoints import bookings_endpoints
from api.articles.endpoints import articles_endpoints
from api.notifications.endpoints import notifications_endpoints
from api.admins.endpoints import admins_endpoints

# Blueprint Registration
app.register_blueprint(auth_endpoints, url_prefix='/api/v1/auth')
app.register_blueprint(admins_endpoints, url_prefix='/api/v1/admins')
app.register_blueprint(users_endpoints, url_prefix='/api/v1/users')
app.register_blueprint(vehicles_endpoints, url_prefix='/api/v1/vehicles')
app.register_blueprint(bookings_endpoints, url_prefix='/api/v1/bookings')
app.register_blueprint(articles_endpoints, url_prefix='/api/v1/articles')
app.register_blueprint(notifications_endpoints, url_prefix='/api/v1/notifications')

# Static Files (Optional)
from static.static_file_server import static_file_server
app.register_blueprint(static_file_server, url_prefix='/static/')

# Main
if __name__ == '__main__':
    app.run(debug=True)
