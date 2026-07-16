"""
app.py
------
YouTube Comments Sentiment Analyzer.

A single-file Streamlit app: paste or upload YouTube comments, and get
each comment classified as Positive / Negative / Neutral, plus an
overall sentiment breakdown.

Run locally with:
    streamlit run app.py
"""

import re
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Sentiment engine (simple lexicon-based analyzer, no external API/model
# downloads needed — works fully offline).
# ---------------------------------------------------------------------------

POSITIVE_WORDS = {
    "good", "great", "awesome", "amazing", "love", "loved", "excellent", "best",
    "fantastic", "wonderful", "helpful", "nice", "perfect", "thanks", "thank",
    "cool", "beautiful", "brilliant", "happy", "enjoyed", "enjoy", "useful",
    "clear", "informative", "superb", "incredible", "impressive", "worth",
    "recommend", "favorite", "favourite", "subscribed", "subscribe", "liked",
    "like", "underrated", "legend", "genius", "fun", "interesting",
    "appreciate", "respect", "proud", "top", "quality", "masterpiece",
}

NEGATIVE_WORDS = {
    "bad", "worst", "hate", "hated", "terrible", "awful", "boring", "waste",
    "poor", "disappointing", "disappointed", "confusing", "confused",
    "annoying", "useless", "dislike", "fake", "scam", "stupid", "dumb",
    "trash", "garbage", "cringe", "misleading", "clickbait", "spam", "wrong",
    "sucks", "suck", "overrated", "unsubscribe", "noise", "lame", "weak",
    "slow", "broken", "unwatchable", "flop",
}

NEGATIONS = {"not", "no", "never", "n't", "don't", "doesn't", "didn't", "isn't", "wasn't"}


def clean_and_tokenize(text: str):
    text = str(text).lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-z0-9'\s]", " ", text)
    return text.split()


def analyze_sentiment(text: str) -> dict:
    tokens = clean_and_tokenize(text)
    if not tokens:
        return {"label": "Neutral", "score": 0.0, "pos_hits": 0, "neg_hits": 0}

    pos_hits, neg_hits = 0, 0
    for i, tok in enumerate(tokens):
        negated = i > 0 and tokens[i - 1] in NEGATIONS
        if tok in POSITIVE_WORDS:
            neg_hits += 1 if negated else 0
            pos_hits += 0 if negated else 1
        elif tok in NEGATIVE_WORDS:
            pos_hits += 1 if negated else 0
            neg_hits += 0 if negated else 1

    score = (pos_hits - neg_hits) / max(len(tokens), 1)
    if pos_hits == neg_hits:
        label = "Neutral"
    elif pos_hits > neg_hits:
        label = "Positive"
    else:
        label = "Negative"

    return {"label": label, "score": round(score, 3), "pos_hits": pos_hits, "neg_hits": neg_hits}


# ---------------------------------------------------------------------------
# Sample data (built in, so the app is demo-able instantly with no upload)
# ---------------------------------------------------------------------------

SAMPLE_COMMENTS = [
    "This video is amazing, I loved it so much! Thanks for sharing.",
    "Worst video ever, complete waste of my time.",
    "It was okay, nothing special honestly.",
    "This is not good at all, very disappointing content.",
    "Great content, very informative and helpful, subscribed!",
    "The editing is so cringe, unsubscribing.",
    "Underrated channel, this deserves way more views.",
    "Can you make a part 2? This was so useful for my exam prep.",
    "Audio quality is terrible, couldn't even watch till the end.",
    "Best tutorial on this topic I have found so far, thank you!",
    "Clickbait title, the video didn't even cover what was promised.",
    "Loved the explanation, very clear and easy to follow.",
    "This is boring, I stopped watching after 2 minutes.",
    "Fantastic work as always, you're a legend!",
    "Not impressed, expected way better quality.",
]


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------

st.set_page_config(page_title="YouTube Sentiment Analyzer", layout="wide")

st.title("YouTube Comments Sentiment Analyzer")
st.caption(
    "Paste YouTube comments (or upload a CSV) to see how viewers really feel — "
    "positive, negative, or neutral — with an overall breakdown."
)

tab1, tab2 = st.tabs(["Paste Comments", "Upload CSV"])

comments = []

with tab1:
    st.write("Paste one comment per line, or click below to load sample data.")
    if st.button("Load sample comments"):
        st.session_state["pasted_text"] = "\n".join(SAMPLE_COMMENTS)

    text_input = st.text_area(
        "Comments (one per line)",
        value=st.session_state.get("pasted_text", ""),
        height=250,
        key="pasted_text",
    )
    if st.button("Analyze Pasted Comments", type="primary"):
        comments = [line.strip() for line in text_input.split("\n") if line.strip()]

with tab2:
    st.write("Upload a CSV file with a column named **comment** (or the first column will be used).")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None and st.button("Analyze CSV Comments", type="primary"):
        df_upload = pd.read_csv(uploaded_file)
        col = "comment" if "comment" in df_upload.columns else df_upload.columns[0]
        comments = df_upload[col].astype(str).tolist()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

if comments:
    results = []
    for c in comments:
        r = analyze_sentiment(c)
        results.append({"Comment": c, "Sentiment": r["label"], "Score": r["score"]})

    df = pd.DataFrame(results)

    st.divider()
    st.subheader("Overall Sentiment Breakdown")

    counts = df["Sentiment"].value_counts()
    total = len(df)
    pos_pct = round(counts.get("Positive", 0) / total * 100, 1)
    neg_pct = round(counts.get("Negative", 0) / total * 100, 1)
    neu_pct = round(counts.get("Neutral", 0) / total * 100, 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Comments", total)
    col2.metric("Positive", f"{pos_pct}%")
    col3.metric("Negative", f"{neg_pct}%")
    col4.metric("Neutral", f"{neu_pct}%")

    st.bar_chart(counts)

    st.divider()
    st.subheader("Comment-by-Comment Results")

    def highlight_sentiment(val):
        color = {"Positive": "#d4f7d4", "Negative": "#f7d4d4", "Neutral": "#f0f0f0"}.get(val, "")
        return f"background-color: {color}"

    st.dataframe(
        df.style.map(highlight_sentiment, subset=["Sentiment"]),
        use_container_width=True,
        height=400,
    )

    csv_out = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download results as CSV", csv_out, "sentiment_results.csv", "text/csv")

else:
    st.info("Paste comments or upload a CSV, then click Analyze to see results.")
    st.markdown(
        """
        ### How it works
        1. **Input** — paste comments (one per line) or upload a CSV of comments.
        2. **Analyze** — each comment is scanned against a curated list of positive
           and negative words (with basic negation handling, e.g. "not good").
        3. **Score** — comments are labeled Positive, Negative, or Neutral based on
           which words matched.
        4. **Report** — an overall breakdown plus a downloadable results table.
        """
    )
