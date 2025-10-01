from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_restx import Api
from flask_socketio import SocketIO
from flask_migrate import Migrate


db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
mail = Mail()
restx_api = Api(
    title='Procurement Workflow API',
    version='1.0',
    description='API for Procurement Workflow Management System',
    doc='/docs',  # Swagger UI
    prefix='/api/v1',
)
socketio = SocketIO(async_mode='threading', cors_allowed_origins='*')
migrate = Migrate()