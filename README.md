# Recursive research factory

A small pipeline that takes a research topic, pulls related arXiv papers and Hugging Face datasets, asks a local LLM for a three-step research plan, scores the idea for novelty and feasibility, and either refines the topic and loops or writes the whole thing out as a Jupyter notebook. There is a Flask dashboard for launching runs and watching the log.

It runs on a local Ollama server (Mistral by default), so no API keys and nothing leaves the machine.

Project page: https://rohitravi.com/projects/hsde

## How a run works

`run_recursive_pipeline.py` is a state machine over a single JSON state dict, persisted after every step so a crashed run resumes where it stopped:

1. `research` — `ResearchAgent` searches arXiv (up to 5 papers, cached per query) and Hugging Face datasets, then checks the topic against a FAISS index of past projects so near-duplicates get rejected. Embeddings come from `all-MiniLM-L6-v2` through sentence-transformers.
2. `execute` — `ExecutionAgent` prompts for a plan: data pipeline, model architecture and training, evaluation metrics.
3. `score` — `score_idea` asks the model for novelty and feasibility scores and a total.
4. `recursive` — `RecursionManager` decides: total of 7 or higher finalizes, novelty under 5 or three iterations stops, otherwise the idea gets refined and the loop runs again.
5. `review` — optional human checkpoint: approve, refine or stop (`HUMAN_REVIEW` in `config.py`).
6. On completion, `OutputAgent` writes a report, `tools/notebook_builder.py` assembles a notebook with the paper links, plan and scaffolded code, and `state_manager.archive_project` moves everything under `projects/<iteration>_<slug>/`.

Thresholds live in `config.py`: `MAX_ITER = 3`, `SCORE_THRESH = 7.0`, `NOVELTY_THRESH = 0.8`.

## What is in the repo

```
run_recursive_pipeline.py     the state machine
state_manager.py              load / save / archive state, with corruption fallback
config.py                     paths and thresholds
agents/                       research, execution, output agents and the recursion manager
tools/                        arxiv search, HF dataset lookup, LLM client with on-disk cache,
                              scoring, notebook builder, code scaffold, project index writer,
                              logger, dashboard helpers, human review prompt
prompts/                      the four prompt templates
web/                          Flask + Socket.IO dashboard (app.py, templates/, static/)
projects/                     archived runs and their notebooks
logs/history.jsonl            one line per completed iteration
PROJECTS_INDEX.md             auto-generated table of past runs
tests/                        pytest coverage for the tools and two of the agents
```

`tools/llm.py` posts to `http://localhost:11434/api/generate` and caches each response by prompt hash under `data/cache/`, so repeated runs are cheap and deterministic.

## Running it

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
ollama serve && ollama pull mistral      # in another shell

python run_recursive_pipeline.py "diffusion models for protein folding"

# or the dashboard
python web/app.py                        # http://localhost:5000
```

`pytest` runs the test suite. `tools/cleanup.py` clears caches and stale project dirs, and `purge_langchain.py` is a one-off script from migrating off the deprecated LangChain embedding wrappers.

## What it actually produced

The runs kept in `projects/` and `logs/history.jsonl` are honest about the limits of the idea. On "structure prediction using diffusion transformers" it scored 8.0 and produced a notebook with a usable three-step plan (PDB/CIF preprocessing, a diffusion transformer, RMSD evaluation against AlphaFold and Rosetta as baselines). Most other runs stalled: the arXiv results drift off-topic when the query is broad (a protein-folding query returning diffusion transformers for image synthesis), the Hugging Face lookup frequently returns "No dataset found", and a plan built on a missing dataset scores below threshold and gets dropped.

So the pipeline mechanics work, and the bottleneck is retrieval quality rather than the loop: paper search by keyword and a dataset lookup by topic string are too weak to seed a plan the scorer will accept. Better retrieval (embedding search over abstracts instead of arXiv's keyword API, a dataset resolver that understands the task type) is where the next effort belongs.
