import re

from inspect_world import load_world, inspect_knowledge


def tokenize(text):
    """Convert English text into a set of lowercase words."""
    return set(re.findall(r"[a-z]+", text.lower()))


def retrieve(world, npc_id, state_id, query, top_k=3):
    # Only search information this NPC is allowed to disclose.
    knowledge = inspect_knowledge(world, npc_id, state_id)
    candidates = knowledge["disclosable"]

    query_tokens = tokenize(query)
    results = []

    for entry in candidates:
        document_tokens = tokenize(entry["text"])

        # Count words shared by the question and the document.
        score = len(query_tokens & document_tokens)

        if score > 0:
            results.append({
                **entry,
                "score": score
            })

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:top_k]


if __name__ == "__main__":
    world = load_world()
    query = "Why are the village gates sealed?"

    for npc_id in ["rowan", "mira"]:
        print(f"\nNPC: {npc_id}")

        results = retrieve(
            world=world,
            npc_id=npc_id,
            state_id="before_trust",
            query=query
        )

        for result in results:
            print(f"  Score: {result['score']}")
            print(f"  Fact: {result['fact_id']}")
            print(f"  Text: {result['text']}")