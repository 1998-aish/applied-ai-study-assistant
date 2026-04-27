import os
import json
from datetime import datetime

LOG_FILE = "logs/activity.log"

def setup_logger():
    """Create logs folder if it doesn't exist."""
    os.makedirs("logs", exist_ok=True)

def log_request(user_input: str, parsed_prefs: dict, recommendations: list):
    """Log every user request and what the AI returned."""
    setup_logger()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "parsed_preferences": parsed_prefs,
        "recommendations": [
            {
                "title": song["title"],
                "artist": song["artist"],
                "score": round(score, 2)
            }
            for song, score, _ in recommendations
        ]
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"📝 Logged to {LOG_FILE}")

def log_error(error_message: str):
    """Log any errors that happen."""
    setup_logger()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "error": error_message
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")