from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == '__main__':
    socketio.init_app(app, cors_allowed_origins=app.config.get('CORS_ORIGINS', '*'))
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)