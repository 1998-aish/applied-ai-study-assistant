# Model Card: AI Music Assistant

---

## 1. Model Name
**AI Music Assistant v2.0**
An extension of VibeFinder 1.0 that adds natural language understanding
powered by Groq (LLaMA 3.3-70b).

---

## 2. Base Project
Built on top of **VibeFinder 1.0** (Module 3 — Music Recommender Simulation).
The original system used manual inputs for genre, mood, energy, and valence.
This version lets users describe what they want in plain English.

---

## 3. What Changed from the Original
| Feature | Original | New |
|---|---|---|
| Input method | Manual genre/mood/energy values | Plain English chat |
| AI used | None — pure math scoring | Groq LLaMA 3.3-70b |
| Explanation | Score breakdown only | Natural language explanation |
| Logging | None | Full activity log |
| Testing | Basic unit tests | Reliability + consistency tests |

---

## 4. How AI Collaboration Was Used
AI tools (Claude) were used to:
- Write the initial structure of `ai_assistant.py`, `logger.py`, `chat.py`
- Debug import errors and data type mismatches
- Suggest the reliability testing approach

Every AI suggestion was reviewed and tested manually. Several times the
AI gave code that worked technically but needed adjustments for this
specific project — for example, the Groq model name needed updating
because the suggested model was decommissioned.

**Key lesson:** AI tools speed up coding but you still need to understand
your own project to catch mistakes.

---

## 5. Known Biases and Limitations

### Energy dominance
Energy is weighted at 4.0 out of 7.5 total points. This means a song
with very high or very low energy will rank near the top regardless of
genre or mood. "Gym Hero" appears in almost every high-energy profile.

### Binary genre/mood matching
"Lofi" and "ambient" are treated as completely different even though they
sound similar. No partial credit for adjacent genres or moods.

### Small catalog
With only 18 songs, the same 3-4 songs appear across many profiles.
Users are never surprised by something new.

### No memory
The system does not remember past conversations or learn from feedback.
Every session starts fresh.

### AI parsing inconsistency
Occasionally the AI returns slightly different energy values for the same
input. Our reliability tests confirm this stays within acceptable bounds.

---

## 6. Testing Results

| Test | Result |
|---|---|
| Same input → same genre | ✅ Passed |
| High energy request → energy > 0.7 | ✅ Passed |
| Chill request → energy < 0.5 | ✅ Passed |
| Always returns 5 songs | ✅ Passed |
| All scores positive | ✅ Passed |
| Top song has highest score | ✅ Passed |

All 6 reliability tests passed consistently.

---

## 7. Ethical Considerations

### Filter bubble
The system always maximises similarity to what the user asked for.
Users are never exposed to music outside their stated taste.
This limits discovery and diversity.

### Transparency
Every recommendation includes a score and reason. Users can see
exactly why each song was suggested. This makes the system explainable.

### No personal data collected
The system does not store user identity, location, or personal details.
Logs only contain the text input and recommendations.

### Intended use
This is a classroom project. It is not intended for commercial use
or deployment in a real music application.

---

## 8. Ideas for Improvement
1. Lower energy weight from 4.0 to 2.0 for more balanced results
2. Add partial credit for similar genres (lofi ≈ ambient)
3. Expand catalog beyond 18 songs
4. Add diversity rule — no same artist twice in top 5
5. Add memory so the system learns from past sessions

---

---

## 9. Reflection and Ethics

### What are the limitations or biases in your system?
The biggest limitation is the small catalog of only 18 songs. This means
the same songs appear repeatedly across different user profiles, creating
a filter bubble. The energy weight (4.0 out of 7.5) dominates scoring,
so high-energy songs like "Gym Hero" appear in almost every energetic
profile regardless of genre. Genre and mood matching is binary — there
is no partial credit for similar genres like lofi and ambient.

### Could your AI be misused, and how would you prevent that?
The system is low-risk since it only recommends music. However, the AI
parsing step could be manipulated with unusual inputs to return wrong
genre/mood values. To prevent this, the code includes a fallback default
if the AI returns invalid JSON. In a real application, input validation
and rate limiting would be added to prevent abuse.

### What surprised you while testing reliability?
The AI was more consistent than expected — it returned the same genre
for identical inputs every time. What was surprising was how confidently
it assigned energy values. For "intense workout music" it returned
energy=1.0 (maximum), and for "calm sleep music" it returned energy=0.2.
The AI understood the emotional context of words like "intense" and
"calm" without being explicitly told what energy means numerically.

### AI Collaboration
**Helpful suggestion:** When switching from Anthropic to Groq, Claude
suggested the complete updated code for `ai_assistant.py` including
the JSON parsing and fallback logic. This saved significant time and
worked correctly on the first try.

**Flawed suggestion:** Claude initially suggested using
`model="llama3-8b-8192"` for Groq, but this model had been
decommissioned. The code ran but returned a 400 error. I had to
manually check the Groq documentation and update it to
`llama-3.3-70b-versatile`. This showed that AI suggestions can be
outdated and always need to be verified.