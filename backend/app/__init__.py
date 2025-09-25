import os
from flask import Flask
from .config import DevelopmentConfig, ProductionConfig, TestingConfig
from .extensions import db, jwt, cors, mail, restx_api, socketio

CONFIG_MAP = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}


def create_app(config_name: str | None = None) -> Flask:
    """Application factory for the Procurement Workflow Management System."""
    app = Flask(__name__)

    env_name = config_name or os.getenv('FLASK_CONFIG', 'development').lower()
    app.config.from_object(CONFIG_MAP.get(env_name, DevelopmentConfig))

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    restx_api.init_app(app)

    # Register API namespaces
    from .api.v1.docs import health_ns, requests_ns, workflow_ns, auth_ns, documents_ns
    restx_api.add_namespace(health_ns, path='/health')
    restx_api.add_namespace(auth_ns, path='/auth')
    restx_api.add_namespace(requests_ns, path='/requests')
    restx_api.add_namespace(workflow_ns, path='/workflow')
    restx_api.add_namespace(documents_ns, path='/documents')

    # Simple index route for sanity
    @app.get('/')
    def index_root():
        return {'service': 'procurement-workflow', 'version': 'v1'}

    # Auto-create tables in dev/testing
    if env_name in ('development', 'testing'):
        with app.app_context():
            # Import models before creating tables
            from . import models  # noqa: F401
            db.create_all()

    return app


__all__ = ['create_app', 'db', 'jwt', 'cors', 'mail', 'restx_api', 'socketio']