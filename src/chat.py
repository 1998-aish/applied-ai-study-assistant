"""
Main chat interface for the AI Music Assistant.
User types in plain English, Claude parses it,
and the recommender returns the best matching songs.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import load_songs, recommend_songs
from src.ai_assistant import parse_user_request, explain_recommendations
from src.logger import log_request, log_error


def run_chat():
    print("=" * 60)
    print("🎵  AI Music Assistant — powered by Claude")
    print("=" * 60)
    print("Tell me what kind of music you want in plain English.")
    print("Type 'quit' to exit.\n")

    songs = load_songs("data/songs.csv")
    print(f"✅ Loaded {len(songs)} songs from catalog.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Thanks for using AI Music Assistant. Bye!")
                break

            if not user_input:
                print("⚠️  Please type something!\n")
                continue

            print("\n🤖 Claude is understanding your request...")
            preferences = parse_user_request(user_input)

            print(f"🎯 Detected: Genre={preferences['preferred_genre']}, "
                  f"Mood={preferences['preferred_mood']}, "
                  f"Energy={preferences['preferred_energy']}, "
                  f"Valence={preferences['preferred_valence']}\n")

            recommendations = recommend_songs(preferences, songs, k=5)

            print("🎶 Top 5 Recommendations:")
            print("-" * 40)
            for rank, (song, score, reasons) in enumerate(recommendations, start=1):
                print(f"#{rank} {song['title']} by {song['artist']}")
                print(f"    Score: {score:.2f}")
                print(f"    Why: {', '.join(reasons)}")
            print()

            top_songs = [song for song, _, _ in recommendations]
            explanation = explain_recommendations(user_input, top_songs)
            print(f"💬 Claude says: {explanation}\n")

            log_request(user_input, preferences, recommendations)
            print("=" * 60 + "\n")

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error: {error_msg}\n")
            log_error(error_msg)


if __name__ == "__main__":
    run_chat()