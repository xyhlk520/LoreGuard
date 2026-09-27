# LoreScope

A State-Aware RAG Dialogue System for NPCs

## Overview

LoreScope is a Python prototype for NPC conversations grounded in
character-specific knowledge and quest-based disclosure rules.

Set in the fictional Moonlight Village, the system separates world
facts from what each NPC knows and what they are currently allowed
to reveal. It filters knowledge by character and player state before
semantic retrieval, then uses the retrieved evidence to generate
dialogue through the Gemini API.

Each NPC has a separate conversation history. History-based query
rewriting helps resolve follow-up questions for retrieval, while the
original player question is retained for response generation.

The project explores how explicit access rules and evidence-grounded
generation can reduce unauthorized disclosure and unsupported claims
in multi-turn NPC dialogue.

## Features

- **Character-specific knowledge:** NPCs have distinct knowledge,
  sources, and beliefs rather than unrestricted access to world facts.
- **Quest-based disclosure:** Knowledge availability depends on
  completed quests in the current player state.
- **Permission-filtered retrieval:** Semantic search operates only
  over facts the current NPC is allowed to disclose.
- **Semantic search:** Uses `all-MiniLM-L6-v2` embeddings and an
  in-memory index to retrieve the top two matching facts.
- **Contextual query rewriting:** Uses conversation history to turn
  follow-up questions into standalone retrieval queries.
- **Independent NPC histories:** Switching characters preserves
  their separate conversations, each retaining up to six messages.
- **Configurable dialogue rules:** Character-specific disclosure
  instructions are defined in configuration rather than hardcoded
  character branches.
- **CLI controls:** `/npc` switches characters; `/state` switches
  predefined player-state snapshots for testing and clears histories
  when the state changes.
- **Evaluation tools:** Includes automated permission and prompt
  tests, labeled retrieval cases, and dialogue logs for manual review.

## Initial Evaluation

| Evaluation | Scope | Result |
|---|---|---|
| Retrieval Hit@2 | 12 manually labeled queries | 10/12 (83.3%) |
| Dialogue behavior | 8 scenarios, 16 turns in one run | All turns manually marked as passing |

Retrieval Hit@2 measures whether at least one expected fact appears
among the top two retrieved results. Each current retrieval case
has one expected fact.

Dialogue review checks predefined behavioral expectations, including
follow-up understanding, source consistency, authorized disclosure,
resistance to player attempts to bypass rules, and handling of
unknown information.

These are small, project-specific evaluations. The results do not
establish general reliability or guarantee that disclosure violations
and unsupported claims cannot occur.

## Known Limitations

- The knowledge base and evaluation sets are small and manually authored.
- Semantic retrieval can miss relevant facts when a query expresses
  an indirect intention or requires inference.
- Retrieval currently uses a fixed top-k without a relevance threshold
  or reranking stage.
- Dialogue quality depends on the external model and may vary between runs.
- Conversation memory is limited to the latest six messages per NPC.
- Player-state switching is a debugging feature, not a gameplay
  system that verifies quest completion.

  ## Setup

### Environment

Developed with Python 3.13.15 on Windows using Conda.
The embedding model runs on CPU; a dedicated GPU is not required.

From the project root, create and activate an environment:

```powershell
conda create -n veilbound python=3.13
conda activate veilbound
python -m pip install -r requirements.txt
```

The first embedding-model load requires internet access to download
the model files. Subsequent runs can use the local cache.

### API Key

Dialogue generation and query rewriting require a Gemini API key.

Set it in the PowerShell session used to run the application:

```powershell
$env:GEMINI_API_KEY = "YOUR_API_KEY"
```

The variable applies to the current terminal session.
Do not commit your API key to the repository.

The Gemini model identifiers are configured in the generation and
query-rewriting code. They must be available to your API account.

## Usage

Start the interactive CLI:

```powershell
python chat.py
```

Enter a message to talk to the current NPC.

| Command | Behavior |
|---|---|
| `/npc` | Show the current NPC and available characters |
| `/npc mira` | Switch to Mira |
| `/npc rowan` | Switch to Rowan |
| `/state` | Show the current player state and available states |
| `/state before_trust` | Select the pre-trust state |
| `/state after_trust` | Select the post-trust state |
| `quit` | Exit the application |

Changing the player state clears all NPC conversation histories.
Switching NPCs preserves their separate histories.

State commands are debugging controls. Claims made in ordinary
dialogue do not complete quests or change the authoritative player state.

## Running Tests and Evaluations

Run all automated permission and prompt tests:

```powershell
python -m unittest discover -v
```

These tests do not call the Gemini API.

Run the retrieval evaluation:

```powershell
python evaluate_retrieval.py
```

This uses `data/retrieval_cases.json` and reports Hit@2 and failed
cases. It requires the embedding model but does not call Gemini.

Run the dialogue evaluation:

```powershell
python evaluate_dialogue.py
```

This uses `data/dialogue_cases.json` and calls Gemini to generate
multi-turn conversations. API usage is subject to account quotas
and any applicable charges.

Results are written to `data/dialogue_results.json`, including
queries, rewritten queries, evidence, responses, and review fields.

Review each turn against its `expected_behavior`:

- `true`: All expected behaviors are satisfied.
- `false`: At least one expected behavior is violated.
- `null`: The turn has not yet been reviewed or needs further judgment.

Add the reason for the judgment in `notes`. Expected behaviors are
evaluation criteria and are not sent to the response-generation model.

The evaluation script overwrites its output file. Preserve existing
results and manual annotations before running it again.