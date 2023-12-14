from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask, jsonify
from sqlalchemy.exc import OperationalError
from bookingapp.config import Config
from flasgger import Swagger
from flask_caching import Cache
import yaml
import os
from flask_mail import Mail
from flask_jwt_extended import JWTManager


db = SQLAlchemy()


# Create an instance of Swagger
swagger = Swagger()

#Create an instance of the cach
cache = Cache()


mail = Mail()  # Create the mail object

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    #app.config.from_object(Config)
    if app.config["SQLALCHEMY_DATABASE_URI"]:
        print("using db")


    # Initialize CORS
    CORS(app, supports_credentials=True)

    @app.errorhandler(OperationalError)
    def handle_db_connection_error(e):
        return jsonify({"error": "Database connection error", "message": str(e)}), 500


    # Load Swagger content from the file
    with open("swagger_config.yaml", "r") as file:
        swagger_config = yaml.load(file, Loader=yaml.FullLoader)
    # Initialize Flasgger with the loaded Swagger configuration
    Swagger(app, template=swagger_config)

    #initialize the caching system
    cache.init_app(app)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Secret key
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587 # 465
    app.config['MAIL_USE_TLS'] = True # False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

    # JWT
    app.config['ACCESS_SECRET_KEY'] = os.getenv('ACCESS_SECRET_KEY')
    app.config['REFRESH_SECRET_KEY'] = os.getenv('REFRESH_SECRET_KEY')

    # Set the JWT_SECRET_KEY in the app configuration
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    jwt = JWTManager(app)  # Instantiate the JWTManager class


    # Initialize Flask-Mail
    mail.init_app(app)  # Initialize Flask-Mail with your app

    # imports blueprints
    from bookingapp.errors.handlers import error
    from bookingapp.auth.authentication import auth_bp
    from bookingapp.utils.utils_routes import util_bp
    from bookingapp.booking.routes import booking_bp
    from bookingapp.user.routes import user_bp
    from bookingapp.admin.routes import admin_bp
    from bookingapp.event.routes import event_bp



    # register blueprint
    app.register_blueprint(error)
    app.register_blueprint(auth_bp)
    app.register_blueprint(util_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(user_bp)


    # create db tables from models if not exists
    with app.app_context():
        db.create_all()

    return app