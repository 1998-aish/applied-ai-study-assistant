# Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeFinder 1.0**

A simple music recommender that matches songs to a listener's mood, energy, and taste.

---

## 2. Goal / Task

VibeFinder suggests songs from a small music catalog based on what a user says they like.

The user tells the system:
- Their preferred **genre** (e.g., lofi, pop, rock)
- Their preferred **mood** (e.g., chill, happy, intense)
- How much **energy** they want in a song (on a scale of 0 to 1)
- How **positive or uplifting** they want the music to feel (also 0 to 1)

The system then scores every song in the catalog and returns the top 5 best matches.

This project is a classroom simulation. It is not intended for real-world use.

---

## 3. Data Used

The catalog contains **18 songs** stored in a CSV file (`data/songs.csv`).

Each song includes the following information:

| Feature | What it means |
|---|---|
| `genre` | The type of music (e.g., lofi, pop, rock, jazz, EDM) |
| `mood` | The emotional tone (e.g., chill, happy, intense, dark, romantic) |
| `energy` | How intense or active the song feels (0 = very calm, 1 = very energetic) |
| `valence` | How positive or happy the song sounds (0 = sad/dark, 1 = bright/uplifting) |
| `tempo_bpm` | The speed of the song in beats per minute |
| `danceability` | How easy the song is to dance to |
| `acousticness` | How acoustic (non-electronic) the song sounds |

**Genre coverage:** lofi, pop, rock, ambient, jazz, synthwave, indie pop, classical, EDM, country, R&B, blues

**Mood coverage:** chill, happy, intense, focused, moody, relaxed, romantic, dark, nostalgic, uplifting, energetic

**Limitation:** Several genres and moods appear only once in the catalog, which means users with niche tastes may not get satisfying results.

---

## 4. Algorithm Summary

The system works by giving each song a **score** based on how closely it matches the user's preferences. The song with the highest score is recommended first.

Here is how the score is calculated:

**Step 1 — Genre match**
If the song's genre matches what the user asked for, it earns **1 point**. If not, it earns 0.

**Step 2 — Mood match**
If the song's mood matches the user's preferred mood, it earns **1 point**. If not, it earns 0.

**Step 3 — Energy similarity**
The system measures how close the song's energy is to what the user wants. A perfect match earns **4 points**. A song that is very far off in energy earns close to 0.

**Step 4 — Valence similarity**
The system measures how close the song's emotional positivity is to what the user wants. A perfect match earns **1.5 points**.

**Final score = genre + mood + energy + valence**

The maximum possible score is **7.5 points**. Songs are ranked from highest to lowest score, and the top 5 are shown to the user along with a short explanation of why each song was chosen.

---

## 5. Observed Behavior and Biases

### What worked well

- **Simple, consistent profiles got good results.** A user who asked for chill lofi music consistently received calm, low-energy songs at the top. A user who asked for high-energy pop consistently received upbeat songs.
- **Obvious mismatches were ranked low.** A quiet acoustic song never appeared at the top for a user wanting intense, high-energy music.
- **The system flagged missing genres.** When a user asked for "metal" — a genre not in the catalog — the system showed a warning instead of silently returning unrelated results.

### What did not work well

- **"Gym Hero" appears too often.** This song has very high energy (0.93 out of 1.0). Because energy is the most heavily weighted feature, it keeps appearing near the top for any user who wants high-energy music — regardless of whether they asked for pop, rock, or EDM. The strong energy weight makes a small number of high-energy songs dominate multiple different profiles.

- **Conflicting preferences produce odd results.** A user who asked for high-energy rock with a dark mood and very low valence (sad/gloomy) still received a slow blues song in the top 3 — simply because that blues song had a matching "dark" mood label. The system cannot recognise that a slow blues track does not satisfy someone who wants aggressive, fast music. It adds up points from each feature separately without understanding how they interact.

- **Missing genres have no fallback.** When a user asks for "metal" and no metal songs exist, the genre score is 0 for every song. The system still returns results, but they are all from wrong genres. There is no logic to suggest the closest available alternative (e.g., rock).

- **Filter bubble — low diversity in results.** Because the catalog only has 18 songs and energy dominates the score, the same 3–4 high-energy or low-energy songs appear repeatedly across different user profiles. Users are never surprised by something unexpected.

---

## 6. Evaluation Process

The system was tested using five hand-crafted user profiles designed to expose different strengths and weaknesses:

| Profile | Purpose |
|---|---|
| High-Energy Pop | Test a typical, well-supported preference |
| Chill Lofi | Test a typical, well-supported preference |
| Intense Rock | Test a genre with limited catalog coverage |
| Conflicting Profile (high energy + dark mood + low valence) | Test contradictory preferences |
| Missing Genre (metal) | Test a genre not present in the catalog |

For each profile, the top 5 recommendations were reviewed and compared to what a human listener would intuitively expect. No numeric accuracy metric was used — evaluation was based on whether the results "made sense."

**Key findings:**
- Clear, consistent profiles produced sensible results
- Energy weight strongly influenced all high-energy profiles
- Conflicting and edge-case profiles revealed the limits of simple score addition
- The catalog was too small to provide meaningful diversity in results

---

## 7. Intended and Non-Intended Use

### Intended use
- A classroom project to explore how content-based recommendation systems work
- A tool for experimenting with feature weights and observing how they change recommendations
- A starting point for learning about AI bias, filter bubbles, and algorithmic fairness

### Not intended for
- Real music applications or production use
- Users with complex, evolving, or contradictory music tastes
- Replacing professional recommendation systems that use listening history or collaborative data
- Any commercial or public-facing deployment

---

## 8. Ideas for Improvement

**1. Lower the energy weight and add partial genre credit**
Energy currently dominates the score at 4.0 out of 7.5 points. Reducing it to around 2.0 would give genre and mood more influence. Adding partial credit for similar genres (e.g., treating "lofi" and "ambient" as related) would also help users with niche tastes find better matches.

**2. Group similar moods together**
Right now, "chill" and "relaxed" are treated as completely different. A user who wants "chill" music gets zero mood points for a "relaxed" song, even though the two feel nearly identical. Grouping adjacent moods (e.g., chill ≈ relaxed ≈ focused) would produce more intuitive results.

**3. Expand the catalog and add diversity logic**
With only 18 songs, the same tracks repeat across almost every profile. Adding more songs — especially for underrepresented genres and moods — would immediately improve variety. A diversity rule that prevents the same artist from appearing more than once in the top 5 would also help avoid repetitive results.

---

## 9. Personal Reflection

My biggest learning moment was when I increased the energy weight and suddenly "Gym Hero" started showing up in almost every profile. I had not expected one small number change to shift the entire behaviour of the system. It made me realise that the weights are not just settings — they are the real decisions behind what the system values. Changing a weight is like changing what the algorithm thinks matters most.

I used AI tools throughout the project to help me write functions, debug errors, and think through edge cases. That was genuinely useful. But I still had to check whether the suggestions made sense for my specific dataset and scoring logic. A few times the AI gave me code that worked technically but did not match what I was actually trying to do. So I learned that AI tools are helpful for speed, but you still have to understand your own project well enough to catch those mistakes.

What surprised me most was how the results sometimes felt like real recommendations, even though the algorithm is just doing simple math. When the Chill Lofi profile returned calm, quiet songs, it felt almost intelligent. But testing the Conflicting Profile quickly broke that illusion. The system had no idea the results did not make sense.

If I extended this project, I would try adding partial credit for similar genres and moods instead of binary matching. I would also experiment with a small diversity rule so the same song cannot appear too many times across different profiles.
