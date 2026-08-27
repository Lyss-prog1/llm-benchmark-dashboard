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
- [ ] Unified test harness (single script, all providers, same prompts)
- [ ] Metrics logging to Weights & Biases
- [ ] Streamlit dashboard

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

## Repository structure

```
src/            application code
.env.example    template for required environment variables (no real values)
requirements.txt   pinned Python dependencies
.pre-commit-config.yaml   gitleaks hook configuration
```
