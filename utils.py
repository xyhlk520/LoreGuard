import json
from pathlib import Path

def load_data(filename):
    path = Path(__file__).resolve().parent / "data" / filename
    with path.open(encoding="utf-8") as file:
        return json.load(file)

def save_game(player_state, event_by_npc):
    path = Path(__file__).resolve().parent / "data" / "saved_game.json"
    with path.open("w", encoding="utf-8") as file:
        json.dump({
            "player_state": player_state,
            "event_by_npc": event_by_npc
        }, file, ensure_ascii=False, indent=2)

def load_saved_game():
    path = Path(__file__).resolve().parent / "data" / "saved_game.json"
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as file:
        return json.load(file)