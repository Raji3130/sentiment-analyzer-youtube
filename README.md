# YouTube Comments Sentiment Analyzer

A tool that classifies YouTube comments as Positive, Negative, or Neutral,
and shows an overall sentiment breakdown for a video.

**Live Demo:** https://sentiment-analyzer-youtube-93zxj8batcxmxvdzyqbtwg.streamlit.app/

## Problem

Creators and viewers often want a quick sense of how a video's comments
are trending — without manually reading through hundreds of them. This
tool automates that by scoring each comment's sentiment and summarizing
the results.

## Features

- Paste comments directly (one per line), or upload a CSV of comments
- Instant sentiment classification: Positive / Negative / Neutral
- Overall breakdown with percentages and a bar chart
- Basic negation handling (e.g. "not good" is correctly read as negative)
- Downloadable results as CSV
- Built-in sample comments for an instant demo — no setup needed

## Tech Stack

- Python
- Streamlit (UI)
- Pandas (data handling)
- A custom lexicon-based sentiment scorer (no external API keys or model
  downloads required — runs fully offline)

## How to Run

1. Clone the repository:
   ```
   git clone https://github.com/<your-username>/youtube-sentiment-analyzer.git
   cd youtube-sentiment-analyzer
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   streamlit run app.py
   ```
4. In the app, click **"Load sample comments"** to try it instantly, or
   paste/upload your own comments.

## How it works

1. **Input** — comments are collected either by pasting text or uploading
   a CSV file with a `comment` column.
2. **Tokenize & clean** — each comment is lowercased, links removed, and
   split into words.
3. **Score** — each word is checked against a curated positive/negative
   word list. A simple negation rule flips the sentiment when a word like
   "not" or "never" comes right before it.
4. **Classify** — comments are labeled based on which sentiment had more
   matches, and an overall breakdown is shown.

## Limitations

- This is a lexicon-based approach (word-matching), not a trained ML
  model — it won't catch sarcasm, slang, or emojis as well as a deep
  learning model (e.g. BERT-based sentiment classifiers) would.
- Only English comments are supported well.
- Comments must be provided manually (paste/CSV) — this version does not
  fetch comments directly from a YouTube video link.

## Future Improvements

- Add YouTube Data API integration to pull comments directly from a video URL
- Swap the lexicon approach for a pretrained transformer model for higher accuracy
- Add emoji-aware sentiment scoring
- Word cloud visualization of most common terms per sentiment 
