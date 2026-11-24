# Architecture

## What this is

A small, educational phishing-message classifier. It takes one short
message as text and returns a label (`phishing-like` or `legitimate`), a
phishing probability, a confidence value, and the words that pushed the
score most toward phishing-like.

It is a portfolio starter, not a production email filter. It was trained
on 24 invented messages, so its only honest use is to show how the
pipeline works and how its limits should be read.

## Pipeline

```
message text
  -> TF-IDF vectorizer (lowercase, English stop words removed, 1-2 grams)
  -> Logistic Regression (max_iter=1000, random_state=42)
  -> predict_proba -> phishing probability
  -> label: phishing-like if probability >= 0.50, else legitimate
  -> explanation: TF-IDF value x model coefficient, ranked, top 5 words
```

Files:

- `src/data.py` – the synthetic dataset, 12 phishing-like and 12
  legitimate invented messages. No real emails, no live data.
- `src/phishing_detector.py` – vectorizer, model, train / predict /
  explain, and the command-line interface.
- `tests/test_detector.py` – 4 unit tests, standard library `unittest`.

## How confidence works, and what it does not mean

- The model outputs `predict_proba` for the phishing class, a number
  between 0.00 and 1.00.
- The decision threshold is 0.50. A score of 0.92 means the model leans
  strongly phishing-like on this tiny training set. A score of 0.51
  means it barely leans that way.
- `confidence` in the output is the distance from 0.50, scaled to
  0.00-1.00. It measures how far the score is from the threshold, not
  how likely the label is true in the real world.
- Confidence is not proof. A confident wrong answer is possible, and
  likely on messages unlike the 24 training examples. In a real SOC
  workflow this score would be one triage signal, checked against
  headers, links, sender reputation, and user reports, never a verdict
  on its own.

## Why Logistic Regression, not a bigger model

- It is explainable: every word has a coefficient, so the top-signals
  list is a real explanation, not a guess.
- It trains in under a second on this data, needs no GPU, and has no
  hidden state.
- Its limits are visible: with 24 examples it will overfit to the
  words in those examples, and it knows nothing about URLs, attachments,
  sender domains, or message headers.

## What a real version would add

1. A labelled dataset collected with consent, with real-world class
   imbalance, not 50/50 synthetic data.
2. Features beyond words: URL structure, domain age, attachment types,
   SPF / DKIM / DMARC results, sender history.
3. Calibration (for example Platt scaling or isotonic regression) and
   evaluation on a held-out set with precision, recall, and a confusion
   matrix, reported by class.
4. A human review queue for scores near the threshold, and logging of
   false positives so the model can be retrained.
5. Privacy and safety review before any real mailbox is connected.

## Safety notes

- Do not point this at a real inbox. It was not built, tested, or
  reviewed for that.
- Do not use it to label real people or real senders as attackers.
- The synthetic messages contain common phishing phrases on purpose,
  for detection training. Do not reuse them to write phishing emails.
