"""
app.py
Flask application entry point for the NexChat Smart Reply ML service.

Responsibilities:
    - Create and configure the Flask app
    - Register the API blueprint from routes.py
    - Start the server

Model training/prediction logic  →  model.py
Training data and templates      →  training_data.py
All route handlers               →  routes.py
"""

from flask import Flask
from flask_cors import CORS
from routes import api


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(api)
    return app


if __name__ == '__main__':
    print("🤖 NexChat Smart Reply Service starting on http://localhost:5001")
    print("   Endpoints: /health  /predict  /predict/debug  /train  /classes")
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=False)
