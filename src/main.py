"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "preferred_genre": "pop",
        "preferred_mood":  "happy",
        "preferred_energy":  0.8,
        "preferred_valence": 0.7,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n--- Top Recommendations ---\n")
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f}")
        for reason in reasons:
            print(f"    • {reason}")
        print()


if __name__ == "__main__":
    main()
