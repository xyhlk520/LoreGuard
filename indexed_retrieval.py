import numpy as np
from sentence_transformers import SentenceTransformer

from inspect_world import load_world, inspect_knowledge
from generation import build_messages

def build_index(world, model):
    """Encode each fact once and store its vector by ID."""
    facts = world["facts"]
    texts = [fact["text"] for fact in facts]

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    index = {}

    for fact, vector in zip(facts, vectors):
        index[fact["id"]] = vector

    return index

def build_document_index(chunks, model):
    if not chunks:
        return {}
    texts = [chunk["embedding_text"] for chunk in chunks]
    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True)
    
    index = {}
    for chunk, vector in zip(chunks, vectors):
        index[chunk["chunk_id"]] = vector

    return index

def retrieve_document_chunks(chunks, model, index, npc_id, player_state, query, top_k=3):

    qualified_chunks = []
    for chunk in chunks:
        knowledge = chunk["knowledge"].get(npc_id)
        if knowledge is None:
            continue

        required_quest = knowledge["disclose_after"]
        if (
            required_quest is None
            or required_quest in player_state["completed_quests"]
        ):
            qualified_chunks.append(chunk)

    if  top_k <= 0 or not qualified_chunks:
        return []

    # Select only vectors for facts this NPC may disclose.
    document_vectors = np.stack([
        index[chunk["chunk_id"]]
        for chunk in qualified_chunks
    ])

    query_vector = model.encode(
        query,
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    scores = document_vectors @ query_vector

    results = []

    for chunk, score in zip(qualified_chunks, scores):
        results.append({
            **chunk,
            "score": float(score)
        })

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:top_k]

def retrieve(world, model, index, npc_id, player_state, query, top_k=3):
    """Search permitted facts using precomputed vectors."""
    knowledge = inspect_knowledge(world, npc_id, player_state)
    candidates = knowledge["disclosable"]

    if not candidates or top_k <= 0:
        return []

    # Select only vectors for facts this NPC may disclose.
    document_vectors = np.stack([
        index[entry["fact_id"]]
        for entry in candidates
    ])

    query_vector = model.encode(
        query,
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    scores = document_vectors @ query_vector

    results = []

    for entry, score in zip(candidates, scores):
        results.append({
            **entry,
            "score": float(score)
        })

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:top_k]


if __name__ == "__main__":
    world = load_world()

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        device="cpu"
    )

    index = build_index(world, model)
    print(f"Indexed {len(index)} facts.")

    npc_id = "mira"
    state_id = "after_trust"

    while True:
        query = input("\nYour question (or 'quit'): ").strip()

        if query.lower() == "quit":
            break

        if not query:
            continue

        results = retrieve(
            world, model, index,
            npc_id, state_id, query
        )

        for result in results:
            print(
                f"\n[{result['fact_id']}] "
                f"score={result['score']:.3f}"
            )
            print(result["text"])