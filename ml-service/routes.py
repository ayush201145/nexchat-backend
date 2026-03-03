"""
routes.py
All Flask route definitions for the Smart Reply ML service.
Imported and registered in app.py.
"""

from flask import Blueprint, request, jsonify
from model import SmartReplyModel
from training_data import TRAINING_SAMPLES

# Module-level model instance (shared across all requests)
_model: SmartReplyModel = None
MODEL_PATH = "smart_reply_model.pkl"

api = Blueprint('api', __name__)


def get_model() -> SmartReplyModel:
    """Return the initialized model, loading or training if needed."""
    global _model
    if _model is None:
        _model = SmartReplyModel()
        if not _model.load(MODEL_PATH):
            _model.train(TRAINING_SAMPLES)
            _model.save(MODEL_PATH)
    return _model


# ── GET /health ───────────────────────────────────────────────────────────────
@api.route('/health', methods=['GET'])
def health():
    """Health check — used by Docker and the Node.js server."""
    m = get_model()
    return jsonify({
        'status':       'ok',
        'model_trained': m.is_trained,
        'classes':      m.classes_,
        'total_classes': len(m.classes_),
    })


# ── POST /predict ─────────────────────────────────────────────────────────────
@api.route('/predict', methods=['POST'])
def predict():
    """
    Main endpoint — returns up to 3 smart reply suggestions.

    Request body:
        { "message": "hey how are you" }

    Response:
        { "message": "...", "suggestions": ["Hey! 👋", "Hi! How's it going?", "Hello there!"] }
    """
    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({'error': 'Request body must include a "message" field'}), 400

    message = data['message']
    if not message or not str(message).strip():
        return jsonify({'message': message, 'suggestions': ['👍', 'Got it!', 'Thanks!']}), 200

    model       = get_model()
    suggestions = model.predict(str(message))

    return jsonify({
        'message':     message,
        'suggestions': suggestions,
    })


# ── POST /predict/debug ───────────────────────────────────────────────────────
@api.route('/predict/debug', methods=['POST'])
def predict_debug():
    """
    Extended prediction with confidence scores — useful for development/testing.

    Response includes label, confidence, top intents, and preprocessed text.
    """
    data = request.get_json(silent=True)
    if not data or 'message' not in data:
        return jsonify({'error': '"message" field required'}), 400

    model  = get_model()
    result = model.predict_with_confidence(str(data['message']))
    return jsonify(result)


# ── POST /train ───────────────────────────────────────────────────────────────
@api.route('/train', methods=['POST'])
def retrain():
    """
    Add new samples and retrain the model.

    Request body:
        {
            "samples": [
                { "text": "sounds perfect", "label": "agree" },
                { "text": "see you tomorrow", "label": "farewell" }
            ]
        }
    """
    data = request.get_json(silent=True)
    if not data or 'samples' not in data:
        return jsonify({'error': '"samples" field required'}), 400

    new_samples = data['samples']
    if not isinstance(new_samples, list) or not new_samples:
        return jsonify({'error': '"samples" must be a non-empty list'}), 400

    # Validate each sample
    for s in new_samples:
        if 'text' not in s or 'label' not in s:
            return jsonify({'error': 'Each sample must have "text" and "label" fields'}), 400

    model      = get_model()
    combined   = TRAINING_SAMPLES + [(s['text'], s['label']) for s in new_samples]
    train_info = model.train(combined)
    model.save(MODEL_PATH)

    return jsonify({
        'success':      True,
        'new_samples':  len(new_samples),
        'total_samples': train_info['samples'],
        'classes':      train_info['classes'],
        'cv_accuracy':  train_info['cv_accuracy'],
    })


# ── GET /classes ──────────────────────────────────────────────────────────────
@api.route('/classes', methods=['GET'])
def get_classes():
    """List all intent classes the model knows about."""
    model = get_model()
    return jsonify({
        'classes': model.classes_,
        'total':   len(model.classes_),
    })
