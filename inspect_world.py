import json
from pathlib import Path
from utils import load_data


def load_world():
    path = Path(__file__).resolve().parent / "data" / "world.json"
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def inspect_knowledge(world, npc_id, player_state):
    facts_by_id = {
        fact["id"]: fact
        for fact in world["facts"]
    }

    character = world["characters"][npc_id]
    completed_quests = set(
        player_state["completed_quests"]
    )

    result = {
        "disclosable": [],
        "withheld": []
    }

    for knowledge in character["knowledge"]:
        fact = facts_by_id[knowledge["fact_id"]]
        required_quest = knowledge["disclose_after"]

        can_disclose = (
            required_quest is None
            or required_quest in completed_quests
        )

        entry = {
            "fact_id": fact["id"],
            "text": fact["text"],
            "source": knowledge["source"],
            "stance": knowledge["stance"]
        }

        category = "disclosable" if can_disclose else "withheld"
        result[category].append(entry)

    return result


if __name__ == "__main__":
    pass