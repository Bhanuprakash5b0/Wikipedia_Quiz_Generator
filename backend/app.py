from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from routes.quiz_routes import quiz_bp
from init_cache import cache

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['CACHE_TYPE']='SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT']=300
    cache.init_app(app)
    quiz_bp.cache=cache

    app.register_blueprint(quiz_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
