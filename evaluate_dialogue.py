import os
import json
from google import genai
from pathlib import Path
from sentence_transformers import SentenceTransformer
from inspect_world import load_world
from chat import rewrite_query
from indexed_retrieval import build_index, retrieve
from generation import build_messages, generate_dialogue

def load_data(filename):
    path = Path(__file__).resolve().parent / "data" / filename
    with path.open(encoding="utf-8") as file:
        return json.load(file)

if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Set GEMINI_API_KEY in this terminal before running."
        )

    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        device="cpu"
    )
    world = load_world()
    index = build_index(world, embedding_model)

    cases = load_data("dialogue_cases.json")
    evaluation_results = []
    with genai.Client(api_key=api_key) as client:
        for case in cases:
            result = {
                "case_id":case["case_id"],
                "npc_id":case["npc_id"],
                "state_id":case["state_id"],
                "turns":[]
            }
            print(f"Case ID: ", case["case_id"])
            npc_id = case["npc_id"]
            state_id = case["state_id"]
            turns = case["turns"]
            history = []
            for cnt, turn in enumerate(turns):
                query = turn["query"].strip()
                if not query:
                    continue

                rewritten_query = rewrite_query(client, query, history)

                evidence = retrieve(
                    world=world,
                    model=embedding_model,
                    index=index,
                    npc_id=npc_id,
                    state_id=state_id,
                    query=rewritten_query,
                    top_k=2
                )

                messages = build_messages(
                world=world,
                npc_id=npc_id,
                state_id=state_id,
                query=query,
                evidence=evidence,
                history=history 
                )

                dialogue = generate_dialogue(client,messages)

                print(f"Turn: ", cnt)
                print(f"User: ", query)
                print(f"\n{world['characters'][npc_id]['name']}: {dialogue}")
                print(f"\nExpected_behavior: ", turn["expected_behavior"])
                print(f"\nRewritten query: ", rewritten_query)

                evi_list = []
                for entry_cnt, entry in enumerate(evidence):
                    evi_list.append({"evidence#":entry_cnt,
                                           "fact_id":entry["fact_id"],
                                           "text":entry["text"],
                                           "score":entry["score"],
                                           "source":entry["source"],
                                           "stance":entry["stance"]})
                    
                    print(f"evidence #",entry_cnt)
                    print(f"id: ", entry["fact_id"])
                    print(f"text: ", entry["text"])
                    print(f"score: ", entry["score"])
                    print("---------------------------------------------")

                result["turns"].append({"query":query,
                        "rewritten_query":rewritten_query,
                        "dialogue":dialogue,
                        "expected_behavior":turn["expected_behavior"],
                        "evidence":evi_list,
                        "reviews":{"passed":None, "notes":""}})  
                
                history.append({"role": "user", "content": query})
                history.append({"role": "assistant", "content": dialogue})
                history = history[-6:]

            evaluation_results.append(result) 
            
            #write to json file
            output_path = Path(__file__).resolve().parent / "data" / "dialogue_results.json"
            with output_path.open("w", encoding="utf-8") as file:
                json.dump(evaluation_results, file, ensure_ascii=False, indent=2) 
