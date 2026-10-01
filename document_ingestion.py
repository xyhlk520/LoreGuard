from pathlib import Path
from utils import load_data
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from generation import build_messages, generate_dialogue
from inspect_world import load_world
from google import genai
import os



def split_markdown_sections(text, document_id):
    chunks = []
    current_section = None
    body_lines = []

    for line in text.splitlines():
        # Skip document title
        if line.startswith("# "):
            continue

        if line.startswith("## "):
            body = "\n".join(body_lines).strip()

            if current_section is not None and body:
                chunks.append({
                    "document_id": document_id,
                    "section": current_section,
                    "text": body
                })

            current_section = line[3:].strip()
            body_lines = []

        elif current_section is not None:
            body_lines.append(line)

    #Save the last section
    body = "\n".join(body_lines).strip()
    if current_section is not None and body:
        chunks.append({
                "document_id": document_id,
                "section": current_section,
                "text": body
            })
    return chunks

def add_chunk_metadata(chunks, document_title, source):
    enriched_chunks = []

    for number, chunk in enumerate(chunks, start=1):
        enriched_chunk = {
            **chunk,
            "chunk_id": f"{chunk['document_id']}_{number:03d}",
            "document_title": document_title,
            "source_file": source,
            "embedding_text": (
                f"{document_title}\n"
                f"{chunk['section']}\n"
                f"{chunk['text']}"
            )
        }
        enriched_chunks.append(enriched_chunk)

    return enriched_chunks

def load_document_chunks(catalog):
    project_root = Path(__file__).resolve().parent
    all_chunks = []
    for document in catalog:
        path = project_root / Path(document["source_file"])
        text = path.read_text(encoding="utf-8")
        chunks = split_markdown_sections(text, document["document_id"])
        enriched_chunks = add_chunk_metadata(chunks, document["title"], str(path))
        for chunk in enriched_chunks:
            chunk["knowledge"] = document["knowledge"]
        all_chunks.extend(enriched_chunks)
    return all_chunks

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

def document_results_to_evidence(results, npc_id):
    evidence = []

    for chunk in results:
        knowledge = chunk["knowledge"][npc_id]

        evidence.append({
            "fact_id": chunk["chunk_id"],
            "text": (
                f"{chunk['document_title']} — {chunk['section']}\n"
                f"{chunk['text']}"
            ),
            "source": knowledge["source"],
            "stance": knowledge["stance"],
            "score": chunk["score"],
            "source_file": chunk["source_file"],
            "section": chunk["section"]
        })

    return evidence


if __name__ == "__main__":
    api_key = os.environ.get("GEMINI_API_KEY")
    world = load_world()
    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        device="cpu"
    )
    player_state = load_data("init_player_state.json")

    catalog = load_data("document_catalog.json")
    chunks = load_document_chunks(catalog)
    index = build_document_index(chunks, model=embedding_model)
    chunk_with_score = retrieve_document_chunks(chunks, model=embedding_model, index=index, npc_id="rowan", player_state=player_state, query="When can I visit the clinic", top_k=3)

    results = retrieve_document_chunks(
        chunks, embedding_model, index,
        "mira", player_state,
        "When can I visit your clinic?",
        top_k=2
    )

    evidence = document_results_to_evidence(results, "mira")

    messages = build_messages(
        world=world,
        npc_id="mira",
        player_state=player_state,
        query="When can I visit your clinic?",
        evidence=evidence
    )
    with genai.Client(api_key=api_key) as client:
        reply = generate_dialogue(client, messages)
        print(reply)