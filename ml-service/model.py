"""
model.py
Naive Bayes NLP model for intent classification and smart reply generation.
Uses scikit-learn's MultinomialNB with a TF-IDF vectorizer pipeline.
"""

import re
import string
import pickle
import os
import numpy as np

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score

from training_data import REPLY_TEMPLATES, FALLBACK_SUGGESTIONS


class SmartReplyModel:
    """
    Multinomial Naive Bayes classifier for chat message intent.

    Pipeline:
        raw text → preprocess → TF-IDF (unigrams + bigrams) → MultinomialNB → intent label → reply templates
    """

    def __init__(self):
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                analyzer='word',
                ngram_range=(1, 2),       # unigrams + bigrams
                max_features=5000,
                stop_words='english',
                sublinear_tf=True,        # apply log normalization to TF
            )),
            ('clf', MultinomialNB(alpha=0.1))  # alpha = Laplace smoothing
        ])
        self.label_encoder = LabelEncoder()
        self.is_trained    = False
        self.classes_      = []

    # ── Preprocessing ─────────────────────────────────────────────────────────
    def preprocess(self, text: str) -> str:
        """Lowercase, remove URLs, strip punctuation, collapse whitespace."""
        text = text.lower().strip()
        text = re.sub(r'http\S+|www\S+', '', text)           # remove URLs
        text = re.sub(r'[^\w\s]', '', text)                  # strip punctuation
        text = re.sub(r'\d+', '', text)                      # remove digits
        text = re.sub(r'\s+', ' ', text).strip()             # collapse spaces
        return text

    # ── Training ──────────────────────────────────────────────────────────────
    def train(self, samples: list[tuple[str, str]]) -> dict:
        """
        Train the model on a list of (text, label) tuples.
        Returns a dict with accuracy info.
        """
        if not samples:
            raise ValueError("Training samples cannot be empty")

        texts, labels = zip(*samples)
        texts         = [self.preprocess(t) for t in texts]
        encoded       = self.label_encoder.fit_transform(labels)
        self.classes_ = list(self.label_encoder.classes_)

        self.pipeline.fit(texts, encoded)
        self.is_trained = True

        # Cross-validation accuracy (3-fold)
        try:
            scores   = cross_val_score(self.pipeline, texts, encoded, cv=3, scoring='accuracy')
            cv_score = round(float(scores.mean()), 4)
        except Exception:
            cv_score = None

        print(f"✅ Model trained — {len(texts)} samples, {len(self.classes_)} classes, CV accuracy: {cv_score}")
        return {
            "samples":    len(texts),
            "classes":    len(self.classes_),
            "cv_accuracy": cv_score,
        }

    # ── Prediction ────────────────────────────────────────────────────────────
    def predict(self, text: str, top_k: int = 3) -> list[str]:
        """
        Predict top-k smart reply suggestions for a given input message.
        Falls back to generic replies if confidence is low.
        """
        if not self.is_trained:
            return FALLBACK_SUGGESTIONS[:top_k]

        processed = self.preprocess(text)
        if not processed:
            return FALLBACK_SUGGESTIONS[:top_k]

        proba       = self.pipeline.predict_proba([processed])[0]
        top_indices = np.argsort(proba)[::-1][:top_k]

        suggestions  = []
        seen         = set()

        for idx in top_indices:
            confidence = proba[idx]
            if confidence < 0.05:
                continue

            label     = self.label_encoder.inverse_transform([idx])[0]
            templates = REPLY_TEMPLATES.get(label, [])

            for template in templates:
                if template not in seen:
                    suggestions.append(template)
                    seen.add(template)
                    break

        # Fill up to top_k with fallbacks
        for fb in FALLBACK_SUGGESTIONS:
            if len(suggestions) >= top_k:
                break
            if fb not in seen:
                suggestions.append(fb)
                seen.add(fb)

        return suggestions[:top_k]

    def predict_with_confidence(self, text: str) -> dict:
        """
        Returns full prediction details including label, confidence, and suggestions.
        Useful for debugging and the /predict/debug endpoint.
        """
        if not self.is_trained:
            return {"label": "unknown", "confidence": 0.0, "suggestions": FALLBACK_SUGGESTIONS[:3]}

        processed   = self.preprocess(text)
        proba       = self.pipeline.predict_proba([processed])[0]
        top_idx     = int(np.argmax(proba))
        label       = self.label_encoder.inverse_transform([top_idx])[0]
        confidence  = round(float(proba[top_idx]), 4)

        # Build ranked list of all intents
        all_intents = [
            {"label": self.label_encoder.inverse_transform([i])[0], "confidence": round(float(p), 4)}
            for i, p in sorted(enumerate(proba), key=lambda x: -x[1])
        ]

        return {
            "input":       text,
            "preprocessed": processed,
            "label":       label,
            "confidence":  confidence,
            "suggestions": self.predict(text),
            "all_intents": all_intents[:5],
        }

    # ── Persistence ───────────────────────────────────────────────────────────
    def save(self, path: str = "model.pkl") -> None:
        """Serialize model to disk."""
        with open(path, 'wb') as f:
            pickle.dump({
                'pipeline':      self.pipeline,
                'label_encoder': self.label_encoder,
                'classes':       self.classes_,
            }, f)
        print(f"💾 Model saved to {path}")

    def load(self, path: str = "model.pkl") -> bool:
        """Load model from disk. Returns True if successful."""
        if not os.path.exists(path):
            return False
        try:
            with open(path, 'rb') as f:
                data = pickle.load(f)
            self.pipeline      = data['pipeline']
            self.label_encoder = data['label_encoder']
            self.classes_      = data.get('classes', [])
            self.is_trained    = True
            print(f"📦 Model loaded from {path} ({len(self.classes_)} classes)")
            return True
        except Exception as e:
            print(f"⚠️  Failed to load model: {e}")
            return False
