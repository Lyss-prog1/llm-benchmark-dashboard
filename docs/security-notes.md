# Security Notes

This document explains the security posture of this project: why it was built
this way, what was tested, and what limitations were found along the way.

## Core principle: billing must be impossible, not just unlikely

No API account used in this project (Mistral, Gemini, Hugging Face) has a
payment method attached. This is the single strongest guarantee against
unexpected charges: without a card on file, a leaked key cannot generate a
bill, no matter how it's misused: the provider simply returns a quota error
once any free allowance is exhausted.

This is treated as the baseline that all other protections below are built
on top of, not a replacement for them.

## Defense in depth

### 1. Local: pre-commit + gitleaks

[`gitleaks`](https://github.com/gitleaks/gitleaks) runs on every `git commit`
via the [`pre-commit`](https://pre-commit.com/) framework (config in
`.pre-commit-config.yaml`, versioned so any clone of this repo gets the same
hook after running `pre-commit install`).

Detection works through two mechanisms:
- **Provider-specific regex patterns** (e.g. Anthropic keys match
  `sk-ant-api03-[A-Za-z0-9_-]{93}AA`) — an exact format match, not a fuzzy
  guess.
- **A generic fallback rule using Shannon entropy**, to catch unlabeled
  secrets while avoiding false positives on ordinary predictable strings.

This was validated with a synthetic, correctly-shaped, high-entropy fake key
(never a real credential) to confirm the hook actually blocks a matching
commit, rather than trusting the setup on faith.

### 2. Remote: GitHub Secret Protection + Push Protection

Both are enabled on this public repository (free for public repos). Secret
Protection passively scans repository content and automatically notifies
partner providers (Mistral, Anthropic, etc.) if one of their token formats is
detected. Push Protection is meant to block a `git push` synchronously before
it reaches the server.

### 3. Environment separation

- `.env` (real keys) is listed in `.gitignore` and never committed.
- `.env.example` documents the expected variable names with no real values.
- API tokens are scoped to the minimum needed (e.g. the Hugging Face token
  is fine-grained, with only "Make calls to Inference Providers" enabled —
  not a broad default-access token).

## Known limitation found during testing

GitHub Push Protection did **not** block a push containing a synthetic,
correctly-formatted, high-entropy fake Anthropic key (`sk-ant-api03-` +
93 random characters + `AA`), even though the same key was correctly
detected and blocked by the local `gitleaks` pre-commit hook.

Most likely explanation: GitHub's provider-partnered detection for push
protection is documented to only support token formats it can identify
"with confidence," which suggests an internal validation stricter than the
publicly known regex pattern (used by gitleaks): plausibly a checksum or
structural check specific to genuinely provider-issued keys.

This could not be fully confirmed without using a real, provider-issued key,
which would defeat the purpose of a safe test. This is treated as an
inherent limitation of testing a proprietary detection system from the
outside, not a configuration mistake: and it's the reason this project does
not rely on push protection as its main line of defense.

## Supply chain note

A real incident is documented against the `mistralai` PyPI package: version
`2.4.6` was never a legitimate release (no matching tag/commit in the
official repository) and contained code that executed on import. It has
since been quarantined by PyPI. This project pins exact dependency versions
in `requirements.txt` (via `pip freeze`) partly to reduce exposure to this
kind of supply-chain risk (installing "whatever is latest" without review
is avoided).
