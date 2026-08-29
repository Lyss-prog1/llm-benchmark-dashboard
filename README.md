# LLM Benchmark Dashboard

A benchmarking tool that compares multiple LLM providers (Mistral, Google Gemini,
Hugging Face) on latency, cost, and response quality — built to support model
selection conversations with enterprise prospects.

Part of a two-project portfolio for a Solutions Engineer / Application Engineer
role, built on a personal Ubuntu 24.04 machine.

## Status

In progress : provider connectivity validated, unified benchmark harness next.

- [x] Security foundation (secret scanning, pre-commit hooks, no-billing-risk setup)
- [x] Individual API connectivity tests (Mistral, Gemini, Hugging Face)
- [x] Unified test harness with enterprise-relevant prompts (sales, financial
      due diligence, HR onboarding)
- [x] Weave integration: automatic tracing, cost tracking, per-provider retry
      with exponential backoff (Gemini)
- [x] Confidentiality metadata per provider (see `docs/security-notes.md`)
- [ ] Quality axis: LLM-as-judge evaluation via `weave.Evaluation`
- [ ] Shareable W&B report
- [ ] Streamlit dashboard

## The four benchmark axes

| Axis | Status | How it's captured |
|---|---|---|
| Latency | Measured end-to-end per call, including retries |
| Cost | Automatic, via Weave's built-in token-based pricing |
| Confidentiality | Static per-provider metadata (`src/provider_metadata.py`) |
| Quality | Planned: LLM-as-judge scoring via Weave Evaluations |


## Observability: Weave, not classic W&B "Models"

This project uses [Weave](https://weave-docs.wandb.ai/), the Weights & Biases
product built for LLM-application observability, rather than the classic
"Models" experiment-tracking product. The reasoning: this project evaluates
calls to already-trained models rather than training a model from scratch —
Weave is designed for exactly that, capturing prompt/response/latency/cost
per call automatically via the `@weave.op` decorator, and will later support
structured quality evaluation.

## Cost safety policy

No account used in this project has a payment method attached. This is a
deliberate architectural choice, not an oversight: without a card on file,
being billed is technically impossible, even if an API key were to leak. This
is treated as a stronger guarantee than any spend-limit setting, since it does
not depend on any detection mechanism working correctly.

Layered protection on top of that baseline:
- `.env` (real keys) is gitignored; `.env.example` documents expected variables
- `pre-commit` + `gitleaks` blocks commits containing secret-shaped strings
- GitHub Secret Protection + Push Protection enabled on this public repo

See [`docs/security-notes.md`](docs/security-notes.md) for the
full reasoning and a known limitation found while testing GitHub Push
Protection.

## Tech stack

| Tool | Role |
|---|---|
| Python 3.12 | Runtime (Python 3.14 was tried first; some SDKs were not yet compatible) |
| Mistral API | Cloud provider #1 |
| Google Gemini API | Cloud provider #2 |
| Hugging Face Inference API | Open-source models provider |
| Weights & Biases | Experiment tracking (planned) |
| Streamlit | Dashboard UI (planned) |

## Setup

```bash
git clone <repo-url>
cd llm-benchmark-dashboard
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# fill in .env with your own API keys (Mistral, Gemini, Hugging Face)
pre-commit install
```

## Running the benchmark

```bash
python3 src/run_benchmark.py
```

Runs every prompt in `src/prompts.py` against all three providers, prints a
summary per call, saves raw results to `results/` (gitignored), and streams
traces to Weave (a project link is printed on first run).

## Repository structure

```
src/
  providers.py           per-provider API call wrappers (call_mistral, call_gemini, call_hf)
  provider_metadata.py   static confidentiality metadata per provider
  prompts.py             fixed enterprise-use-case prompts (sales, finance, HR)
  run_benchmark.py       entry point: runs all prompts x all providers, logs to Weave
docs/
  security-notes.md      threat model, defense in depth, known limitations
.env.example              template for required environment variables (no real values)
requirements.txt          pinned Python dependencies
.pre-commit-config.yaml   gitleaks hook configuration
```
