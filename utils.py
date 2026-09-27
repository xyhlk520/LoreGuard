import json
from pathlib import Path

def load_data(filename):
    path = Path(__file__).resolve().parent / "data" / filename
    with path.open(encoding="utf-8") as file:
        return json.load(file)