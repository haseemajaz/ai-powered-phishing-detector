"""AI-powered phishing detector, educational starter.

Trains a TF-IDF + Logistic Regression classifier on synthetic demo messages
only (see data.py). No real phishing emails, no live data.

Usage:
    python -m src.phishing_detector --train
    python -m src.phishing_detector --predict "Urgent: verify your account now"
    python -m src.phishing_detector --demo

How confidence works:
    predict_proba returns the model's probability for the phishing class.
    0.50 is the decision threshold. A score near 0.50 means the model is
    unsure, a score near 1.00 or 0.00 means it is confident, but confidence
    is not proof. It is a calibrated-looking output from a small demo model
    trained on 24 invented messages, so treat it as a signal to investigate,
    never as a verdict on its own. See docs/architecture.md.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from src.data import SYNTHETIC_MESSAGES

LABELS = {0: "legitimate", 1: "phishing-like"}


def build_model():
    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2))
    model = LogisticRegression(max_iter=1000, random_state=42)
    return vectorizer, model


def train():
    texts = [text for _, text in SYNTHETIC_MESSAGES]
    labels = [label for label, _ in SYNTHETIC_MESSAGES]
    vectorizer, model = build_model()
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.25, random_state=42, stratify=labels
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    model.fit(X_train_vec, y_train)
    accuracy = accuracy_score(y_test, model.predict(vectorizer.transform(X_test)))
    return vectorizer, model, accuracy, classification_report(
        y_test, model.predict(vectorizer.transform(X_test)),
        target_names=["legitimate", "phishing-like"], zero_division=0,
    )


def train_full():
    """Train on all synthetic messages, for prediction use."""
    texts = [text for _, text in SYNTHETIC_MESSAGES]
    labels = [label for label, _ in SYNTHETIC_MESSAGES]
    vectorizer, model = build_model()
    model.fit(vectorizer.fit_transform(texts), labels)
    return vectorizer, model


def explain(vectorizer, model, text, top_n=5):
    """Return the words that pushed the score most toward phishing-like."""
    vec = vectorizer.transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = vec.toarray()[0] * model.coef_[0]
    ranked = sorted(
        ((score, feature_names[i]) for i, score in enumerate(scores) if score != 0),
        reverse=True,
    )
    return [(word, round(float(score), 3)) for score, word in ranked[:top_n]]


def predict(vectorizer, model, text):
    proba = model.predict_proba(vectorizer.transform([text]))[0]
    phishing_prob = float(proba[1])
    return {
        "text": text,
        "label": LABELS[1] if phishing_prob >= 0.5 else LABELS[0],
        "phishing_probability": round(phishing_prob, 3),
        "confidence": round(abs(phishing_prob - 0.5) * 2, 3),
        "top_signals": explain(vectorizer, model, text),
    }


def main():
    parser = argparse.ArgumentParser(description="Phishing detector (synthetic demo data only)")
    parser.add_argument("--train", action="store_true", help="Train and show test accuracy")
    parser.add_argument("--predict", type=str, help="Classify one message")
    parser.add_argument("--demo", action="store_true", help="Run the built-in demo messages")
    args = parser.parse_args()

    if args.train:
        _, _, accuracy, report = train()
        print(f"Test accuracy on held-out synthetic messages: {accuracy:.2f}")
        print(report)
        return

    vectorizer, model = train_full()

    if args.predict:
        result = predict(vectorizer, model, args.predict)
        print(f"Label: {result['label']}")
        print(f"Phishing probability: {result['phishing_probability']}")
        print(f"Confidence (distance from 0.50): {result['confidence']}")
        print("Top signals pushing toward phishing-like:")
        for word, score in result["top_signals"] or [("(none)", 0.0)]:
            print(f"  {word}: {score}")
        return

    if args.demo:
        for label, text in SYNTHETIC_MESSAGES[:6]:
            result = predict(vectorizer, model, text)
            print(f"[{result['label']}] p={result['phishing_probability']}  {text[:80]}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
