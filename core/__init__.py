from flask import Flask
import os

def create_app():
    """Application factory with absolute path hardening for Vercel."""
    # Absolute paths are required for Vercel serverless functions
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(base_dir, '..', 'templates')
    static_dir = os.path.join(base_dir, '..', 'static')

    app = Flask(__name__, 
                template_folder=template_dir, 
                static_folder=static_dir)
    
    # Register Routes from the new 'core' package
    from core.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
