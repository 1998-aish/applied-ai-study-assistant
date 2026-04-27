import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def parse_user_request(user_input: str) -> dict:
    """
    Send plain English request to Groq.
    Groq returns genre, mood, energy, valence as JSON.
    """
    prompt = f"""
You are a music preference parser. A user describes what music they want.
Extract their preferences and return ONLY a JSON object with these exact keys:
- preferred_genre: one of [lofi, pop, rock, ambient, jazz, synthwave, indie pop, classical, EDM, country, R&B, blues]
- preferred_mood: one of [chill, happy, intense, focused, moody, relaxed, romantic, dark, nostalgic, uplifting, energetic]
- preferred_energy: a float between 0.0 and 1.0
- preferred_valence: a float between 0.0 and 1.0

User request: "{user_input}"

Return ONLY the JSON. No explanation. No extra text. No markdown.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        preferences = json.loads(raw)
        return preferences
    except json.JSONDecodeError:
        print(f"⚠️  Warning: Could not parse AI response: {raw}")
        return {
            "preferred_genre": "pop",
            "preferred_mood": "happy",
            "preferred_energy": 0.5,
            "preferred_valence": 0.5
        }


def explain_recommendations(user_input: str, songs: list) -> str:
    """
    Ask Groq to explain the recommendations in plain English.
    """
    song_list = "\n".join([
        f"- {s['title']} by {s['artist']} ({s['genre']}, {s['mood']})"
        for s in songs
    ])

    prompt = f"""
A user asked for: "{user_input}"

The music recommender returned these top songs:
{song_list}

In 2-3 sentences, explain why these songs are a good match for what the user asked for.
Be friendly and conversational.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()