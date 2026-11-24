"""Tests for the phishing detector. Run: python -m unittest discover -s tests -v"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.phishing_detector import predict, train_full


class TestDetector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vectorizer, cls.model = train_full()

    def test_phishing_like_message_scores_high(self):
        result = predict(
            self.vectorizer, self.model,
            "Urgent: your account will be suspended, verify now by clicking the link",
        )
        self.assertEqual(result["label"], "phishing-like")
        self.assertGreaterEqual(result["phishing_probability"], 0.5)

    def test_legitimate_message_scores_low(self):
        result = predict(
            self.vectorizer, self.model,
            "Hi team, here are the notes from today's meeting",
        )
        self.assertEqual(result["label"], "legitimate")
        self.assertLess(result["phishing_probability"], 0.5)

    def test_probability_is_between_zero_and_one(self):
        result = predict(self.vectorizer, self.model, "Hello, please review the document")
        self.assertGreaterEqual(result["phishing_probability"], 0.0)
        self.assertLessEqual(result["phishing_probability"], 1.0)

    def test_explanation_returns_signals(self):
        result = predict(
            self.vectorizer, self.model,
            "Congratulations, you have won a prize, claim your reward now",
        )
        self.assertIsInstance(result["top_signals"], list)


if __name__ == "__main__":
    unittest.main()
