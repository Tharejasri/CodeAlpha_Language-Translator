from flask import Flask, send_from_directory
from flask_cors import CORS
from .routes import api_bp
import os

def create_app():
    app = Flask(__name__, static_folder='../../frontend')
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Serve frontend
    @app.route('/')
    def serve_frontend():
        return send_from_directory('../../frontend', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('../../frontend', path)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)