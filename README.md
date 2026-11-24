# AI-Powered Phishing Detector

Classify a short message as `phishing-like` or `legitimate`, and explain
the model's confidence in plain language.

This is project 13 of 13 in a security portfolio series, in the AI and
Security area. It is an educational starter, built to show how a
detection model works and how its limits should be read, not a production
email filter.

> Safety: this project trains on 24 synthetic demo messages that were
> invented for this repo. There are no real phishing emails, no real
> inboxes, and no live data here. Do not point it at a real mailbox.

## What it does

- Trains a TF-IDF + Logistic Regression classifier on the synthetic
  messages in `src/data.py` (12 phishing-like, 12 legitimate).
- Classifies one message from the command line and prints:
  - the label, `phishing-like` or `legitimate`
  - the phishing probability, 0.00 to 1.00
  - a confidence value, how far the score is from the 0.50 threshold
  - the top 5 words that pushed the score toward phishing-like, with
    their contribution scores
- Ships with 4 unit tests and architecture notes in `docs/`.

## How to run

```bash
cd ai-powered-phishing-detector
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Train and show test accuracy on held-out synthetic messages
python -m src.phishing_detector --train

# Classify one message
python -m src.phishing_detector --predict "Urgent: your account will be suspended, verify now by clicking the link"

# Run the built-in demo
python -m src.phishing_detector --demo

# Run the tests
python -m unittest discover -s tests -v
```

## Example output

```
$ python -m src.phishing_detector --predict "Urgent: your account will be suspended, verify now by clicking the link"
Label: phishing-like
Phishing probability: 0.603
Confidence (distance from 0.50): 0.206
Top signals pushing toward phishing-like:
  account: 0.076
  link: 0.072
  verify: 0.056
  verify clicking: 0.034
  urgent account: 0.034
```

Verified 22 Nov 2026 on this machine, scikit-learn 1.9.1, Python 3.12.3.
Held-out test accuracy was 0.83 on 6 synthetic messages, and all 4 unit
tests pass. Note the probability is only 0.603, close to the 0.50
threshold, which is exactly why the confidence explanation matters: this
small demo model is not very sure, even when it gets the label right.

## How model confidence works

- The model outputs a probability for the phishing class. 0.50 is the
  decision threshold.
- A score near 0.50 means the model is unsure. A score near 1.00 or
  0.00 means it is confident on this tiny training set.
- Confidence is not proof. A confident wrong answer is possible, and
  likely on messages unlike the 24 training examples. In a real SOC
  workflow this score would be one triage signal, checked against
  headers, links, sender reputation, and user reports, never a verdict
  on its own.
- See `docs/architecture.md` for the full explanation, including why
  Logistic Regression was chosen and what a real version would add.

## What an employer sees

- A complete, runnable project, not a list of tools studied.
- A model chosen for explainability, with a real explanation for every
  prediction, not a black box.
- Honest evaluation: training accuracy is reported on held-out synthetic
  messages, and the limits of 24 invented examples are stated in the
  README and in the architecture notes.
- Safety awareness: no real phishing data, no live mailbox, and a clear
  note on what a production version would need before it touched real
  email (consent, calibration, human review, privacy review).

## Project structure

```
ai-powered-phishing-detector/
  README.md
  requirements.txt
  src/
    phishing_detector.py   # TF-IDF + Logistic Regression, CLI, explain()
    data.py                # 24 synthetic demo messages, labelled
  tests/
    test_detector.py       # 4 unit tests (unittest)
  docs/
    architecture.md        # pipeline, confidence, limits, next steps
```

## Next steps

- Add a held-out evaluation with precision, recall, and a confusion
  matrix, reported by class.
- Add URL and sender-domain features, and a human review queue for
  scores near 0.50.
- Replace the synthetic data with a properly licensed, consented
  dataset before any real-world use.
