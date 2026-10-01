import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from inspect_world import load_world
from indexed_retrieval import build_index, retrieve
from utils import load_data

def load_data(filename):
    path = Path(__file__).resolve().parent / "data" / filename
    with path.open(encoding="utf-8") as file:
        return json.load(file)

if __name__ == "__main__":

    world = load_world()
    cases = load_data("retrieval_cases.json")
    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        device="cpu"
    )
    index = build_index(world,model)
    hits = 0
    failed_cases = []
    for case in cases:
        results = retrieve(world, model, index, 
                        case["npc_id"], case["state_id"],
                        case["query"],top_k=2)
        retrieved = [result["fact_id"] for result in results]
        expected = set(case["expected_fact_ids"])
        isHit = not expected.isdisjoint(retrieved)
        if isHit:
            hits += 1
        else:
            failed_cases.append({**case,
                                "retrieved": retrieved})

        print(f"Case: ", case["case_id"])
        print(f"Expected: ", case["expected_fact_ids"])
        print(f"Retrieved: ", retrieved)
        print(f"Hit:", "True" if isHit else "False")

    if cases:
        print(f"Hit@2: {hits}/{len(cases)} = {hits / len(cases):.1%}")
        print("Failed Cases: ")
        for case in failed_cases:
            print(f"Case: ", case["case_id"])
            print(f"Expected: ", case["expected_fact_ids"])
            print(f"Retrieved:", case["retrieved"])
            candidates = retrieve(world, model, index, case["npc_id"],
                                  case["state_id"], case["query"], top_k=10)
            for candidate in candidates:
                print(f"fact: ", candidate["fact_id"])
                print(f"score: ", candidate["score"])
    else:   
        print("No evaluation cases found.")
        


