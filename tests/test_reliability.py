"""
Reliability tests for the AI Music Assistant.
Tests if the AI gives consistent results for the same input.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ai_assistant import parse_user_request
from src.recommender import load_songs, recommend_songs


def test_same_input_gives_same_genre():
    """Same input should always return the same genre."""
    input1 = parse_user_request("I want chill lofi music for studying")
    input2 = parse_user_request("I want chill lofi music for studying")
    assert input1["preferred_genre"] == input2["preferred_genre"], \
        f"Genre changed: {input1['preferred_genre']} vs {input2['preferred_genre']}"
    print(f"✅ Genre consistent: {input1['preferred_genre']}")


def test_high_energy_request_gives_high_energy():
    """High energy request should always return energy > 0.7."""
    result = parse_user_request("I want intense high energy workout music")
    assert float(result["preferred_energy"]) > 0.7, \
        f"Expected energy > 0.7, got {result['preferred_energy']}"
    print(f"✅ High energy detected: {result['preferred_energy']}")


def test_chill_request_gives_low_energy():
    """Chill request should always return energy < 0.5."""
    result = parse_user_request("I want calm relaxing sleep music")
    assert float(result["preferred_energy"]) < 0.5, \
        f"Expected energy < 0.5, got {result['preferred_energy']}"
    print(f"✅ Low energy detected: {result['preferred_energy']}")


def test_recommender_always_returns_5_songs():
    """Recommender should always return exactly 5 songs."""
    songs = load_songs("data/songs.csv")
    prefs = {
        "preferred_genre": "pop",
        "preferred_mood": "happy",
        "preferred_energy": 0.8,
        "preferred_valence": 0.8
    }
    results = recommend_songs(prefs, songs, k=5)
    assert len(results) == 5, f"Expected 5 songs, got {len(results)}"
    print(f"✅ Always returns 5 songs")


def test_scores_are_always_positive():
    """All recommendation scores should be positive."""
    songs = load_songs("data/songs.csv")
    prefs = {
        "preferred_genre": "lofi",
        "preferred_mood": "chill",
        "preferred_energy": 0.3,
        "preferred_valence": 0.6
    }
    results = recommend_songs(prefs, songs, k=5)
    for song, score, _ in results:
        assert score > 0, f"Score should be positive, got {score}"
    print(f"✅ All scores are positive")


def test_top_song_has_highest_score():
    """First song should always have the highest score."""
    songs = load_songs("data/songs.csv")
    prefs = {
        "preferred_genre": "EDM",
        "preferred_mood": "energetic",
        "preferred_energy": 0.9,
        "preferred_valence": 0.8
    }
    results = recommend_songs(prefs, songs, k=5)
    scores = [score for _, score, _ in results]
    assert scores[0] == max(scores), "Top song should have highest score"
    print(f"✅ Top song has highest score: {scores[0]:.2f}")


if __name__ == "__main__":
    print("Running reliability tests...\n")
    test_same_input_gives_same_genre()
    test_high_energy_request_gives_high_energy()
    test_chill_request_gives_low_energy()
    test_recommender_always_returns_5_songs()
    test_scores_are_always_positive()
    test_top_song_has_highest_score()
    print("\n✅ All reliability tests passed!")