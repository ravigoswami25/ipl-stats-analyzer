# analyzer/loader.py
# Responsibility: Load JSON data from files safely

import json
from pathlib import Path

# Base path — always points to data/ folder
DATA_DIR = Path(__file__).parent.parent / "data"

def load_players() -> list[dict]:
    """
    Load all players from players.json
    Returns list of player dicts
    """
    file_path = DATA_DIR / "players.json"

    try:
        with open(file_path, "r") as f:
            players = json.load(f)
        print(f"✅ Loaded {len(players)} players")
        return players

    except FileNotFoundError:
        print(f"❌ Error: players.json not found at {file_path}")
        return []

    except json.JSONDecodeError:
        print("❌ Error: players.json is not valid JSON")
        return []


def load_matches() -> list[dict]:
    """
    Load all matches from matches.json
    Returns list of match dicts
    """
    file_path = DATA_DIR / "matches.json"

    try:
        with open(file_path, "r") as f:
            matches = json.load(f)
        print(f"✅ Loaded {len(matches)} matches")
        return matches

    except FileNotFoundError:
        print(f"❌ Error: matches.json not found at {file_path}")
        return []

    except json.JSONDecodeError:
        print("❌ Error: matches.json is not valid JSON")
        return []


def save_results(data: dict) -> None:
    """
    Save analysis results to results.json
    """
    file_path = DATA_DIR / "results.json"

    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Results saved to {file_path}")

    except Exception as e:
        print(f"❌ Error saving results: {e}")