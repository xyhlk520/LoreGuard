import json
from pathlib import Path


def load_world():
    path = Path(__file__).resolve().parent / "data" / "world.json"
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def inspect_knowledge(world, npc_id, state_id):
    facts_by_id = {
        fact["id"]: fact
        for fact in world["facts"]
    }

    character = world["characters"][npc_id]
    completed_quests = set(
        world["player_states"][state_id]["completed_quests"]
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
    world = load_world()

    for npc_id in world["characters"]:
        for state_id in world["player_states"]:
            result = inspect_knowledge(world, npc_id, state_id)

            print(f"\n{npc_id} | {state_id}")

            for category, entries in result.items():
                fact_ids = [entry["fact_id"] for entry in entries]
                print(f"  {category}: {fact_ids}")