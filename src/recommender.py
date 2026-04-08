import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Load songs from a CSV file and return a list of dictionaries with proper data types.
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":            int(row["id"]),
                "title":         row["title"],
                "artist":        row["artist"],
                "genre":         row["genre"],
                "mood":          row["mood"],
                "energy":        float(row["energy"]),
                "tempo_bpm":     int(row["tempo_bpm"]),
                "valence":       float(row["valence"]),
                "danceability":  float(row["danceability"]),
                "acousticness":  float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Compute a weighted score and explanation for how well a song matches user preferences.
    """
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["preferred_genre"]:
        score += 1.0
        reasons.append("genre match (+1.0)")

    if song["mood"] == user_prefs["preferred_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_sim = (1 - abs(song["energy"] - user_prefs["preferred_energy"])) * 4.0
    score += energy_sim
    reasons.append(f"energy similarity (+{energy_sim:.1f})")

    valence_sim = (1 - abs(song["valence"] - user_prefs["preferred_valence"])) * 1.5
    score += valence_sim
    reasons.append(f"valence similarity (+{valence_sim:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Rank songs by relevance and return the top k recommendations with scores and reasons.
    """
    scored = [
        {"song": song, "score": score, "reasons": reasons}
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)

    return [(entry["song"], entry["score"], entry["reasons"]) for entry in ranked[:k]]
