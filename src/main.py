"""
Command line runner for the Music Recommender Simulation.

Runs multiple user profiles sequentially to stress-test the recommender.
Scoring logic lives in recommender.py — this file handles evaluation only.
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles for stress testing
# ---------------------------------------------------------------------------

PROFILES = [
    (
        "High-Energy Pop",
        {
            "preferred_genre":   "pop",
            "preferred_mood":    "happy",
            "preferred_energy":  0.9,
            "preferred_valence": 0.85,
        },
    ),
    (
        "Chill Lofi",
        {
            "preferred_genre":   "lofi",
            "preferred_mood":    "chill",
            "preferred_energy":  0.4,
            "preferred_valence": 0.6,
        },
    ),
    (
        "Intense Rock",
        {
            "preferred_genre":   "rock",
            "preferred_mood":    "intense",
            "preferred_energy":  0.92,
            "preferred_valence": 0.45,
        },
    ),
    (
        "Conflicting Profile (high energy + dark mood + low valence)",
        {
            "preferred_genre":   "rock",
            "preferred_mood":    "dark",
            "preferred_energy":  0.95,
            "preferred_valence": 0.1,
        },
    ),
    (
        "Missing Genre (metal — not in dataset)",
        {
            "preferred_genre":   "metal",
            "preferred_mood":    "intense",
            "preferred_energy":  0.99,
            "preferred_valence": 0.2,
        },
    ),
]


# ---------------------------------------------------------------------------
# Helper: run and display one profile
# ---------------------------------------------------------------------------

def run_profile(profile_name: str, user_prefs: dict, songs: list) -> None:
    print(f"\n>> Profile: {profile_name}")
    print(f"   Genre={user_prefs['preferred_genre']}  "
          f"Mood={user_prefs['preferred_mood']}  "
          f"Energy={user_prefs['preferred_energy']}  "
          f"Valence={user_prefs['preferred_valence']}")
    print("-" * 60 + "\n")

    genres_in_catalog = {song["genre"] for song in songs}
    if user_prefs["preferred_genre"] not in genres_in_catalog:
        print(f"  ⚠  Warning: genre '{user_prefs['preferred_genre']}' not found in catalog.")
        print(f"     Genre match score will be 0 for all songs.\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {', '.join(reasons)}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.\n")
    print("=" * 60)

    for profile_name, user_prefs in PROFILES:
        run_profile(profile_name, user_prefs, songs)
        print("=" * 60)


if __name__ == "__main__":
    main()
