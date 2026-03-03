from flask import Flask
from flask_cors import CORS
from routes import api

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api)
    return app

# Module-level app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    print("🤖 NexChat Smart Reply Service starting on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
