# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

This is a **content-based recommender**: it compares the features of each song directly against a user’s stated preferences to produce a ranked list of suggestions. No listening history or other users’ data is involved — recommendations are driven entirely by song attributes and profile values.

### Input → Process → Output

```
User Profile  ──┐
                ├──▶  Score every song  ──▶  Sort by score  ──▶  Top K songs
songs.csv     ──┘
```

### Data Flow

1. **User Profile** — The user provides four preferences:
   - `preferred_genre` (e.g., `”lofi”`)
   - `preferred_mood` (e.g., `”chill”`)
   - `preferred_energy` — a float between 0.0 and 1.0
   - `preferred_valence` — a float between 0.0 and 1.0

2. **Read songs.csv** — The catalog is loaded from `data/songs.csv`. Each row represents one song with features: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.

3. **Loop through each song** — Every song in the catalog is evaluated against the user profile independently.

4. **Score each song** — A total score is calculated from four weighted components (see Scoring Logic below).

5. **Sort and select** — All songs are sorted by score in descending order. The top K highest-scoring songs are returned as recommendations.

---

### Scoring Logic

Each song receives a score out of a maximum of **7.5 points**, calculated as follows:

| Component | Method | Max Points |
|---|---|---|
| Genre match | +2.0 if `song.genre == user.preferred_genre`, else 0 | 2.0 |
| Mood match | +1.0 if `song.mood == user.preferred_mood`, else 0 | 1.0 |
| Energy similarity | `(1 − \|song.energy − user.energy\|) × 2.0` | 2.0 |
| Valence similarity | `(1 − \|song.valence − user.valence\|) × 1.5` | 1.5 |

#### Final Scoring Formula

```
score = (genre_match × 2.0)
      + (mood_match  × 1.0)
      + (1 − |song.energy  − user.energy|)  × 2.0
      + (1 − |song.valence − user.valence|) × 1.5
```

**Example** — User profile: `lofi, chill, energy=0.4, valence=0.6`

| Song | Genre | Mood | Energy | Valence | Score |
|---|---|---|---|---|---|
| Library Rain (lofi, chill, 0.35, 0.60) | 2.0 | 1.0 | 1.90 | 1.50 | **6.40** |
| Spacewalk Thoughts (ambient, chill, 0.28, 0.65) | 0.0 | 1.0 | 1.76 | 1.43 | **4.19** |
| Storm Runner (rock, intense, 0.91, 0.48) | 0.0 | 0.0 | 0.98 | 1.32 | **2.30** |

---

### Why These Weights?

- **Genre (2.0) — highest weight.** Genre is the strongest categorical signal. A rock song and a lofi track are fundamentally different listening experiences regardless of their numerical features. Mismatched genre should dominate the penalty.

- **Energy (2.0) — tied for highest.** Energy spans the full 0.0–1.0 range across the catalog (e.g., ambient at 0.28 vs. EDM at 0.95). It is the single most discriminating numerical feature and deserves equal weight to genre.

- **Valence (1.5) — medium weight.** Valence is useful but noisier — many genres cluster in the 0.55–0.85 range, so differences are often small. It acts as a meaningful tiebreaker without overriding stronger signals.

- **Mood (1.0) — lowest weight.** Mood is partially correlated with genre and energy. Giving it less weight avoids double-penalizing songs that already lost points on genre.

---

### Limitations and Potential Biases

- **Genre bias.** Genre is a binary match — a song is either in or out. Perceptually similar genres (e.g., `lofi` and `ambient`) are treated as completely different, which can unfairly suppress good recommendations.

- **Filter bubble effect.** Because the system always maximizes similarity to the stated profile, it will consistently surface the same cluster of songs. Users are never exposed to songs outside their declared taste, which prevents serendipitous discovery.

- **Limited feature usage.** Three features in `songs.csv` — `tempo_bpm`, `danceability`, and `acousticness` — are not used in scoring. These carry meaningful information (e.g., acousticness strongly separates lofi from EDM) and represent unused signal.

- **No collaborative filtering.** The system has no knowledge of what other users enjoy. It cannot surface a hidden gem that users with similar profiles consistently love, which is one of the most powerful techniques in production recommenders like Spotify or Netflix.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

```

---
## 10. Example Output

![CLI Output](images/output.png)

