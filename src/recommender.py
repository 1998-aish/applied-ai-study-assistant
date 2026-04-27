import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
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
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        return "Explanation placeholder"


def load_songs(csv_path: str) -> List[Dict]:
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["preferred_genre"]:
        score += 1.0
        reasons.append("genre match (+1.0)")

    if song["mood"] == user_prefs["preferred_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    song_energy = float(song["energy"])
    user_energy = float(user_prefs["preferred_energy"])
    energy_sim = (1 - abs(song_energy - user_energy)) * 4.0
    score += energy_sim
    reasons.append(f"energy similarity (+{energy_sim:.1f})")

    song_valence = float(song["valence"])
    user_valence = float(user_prefs["preferred_valence"])
    valence_sim = (1 - abs(song_valence - user_valence)) * 1.5
    score += valence_sim
    reasons.append(f"valence similarity (+{valence_sim:.1f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append({"song": song, "score": score, "reasons": reasons})

    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)
    return [(entry["song"], entry["score"], entry["reasons"]) for entry in ranked[:k]]