PROVIDER_METADATA = {
    "mistral": {
        "confidentiality": "cloud",
        "confidentiality_note": (
            "Data sent to Mistral's API (EU-based company). Paid tiers "
            "commit to not training on customer data; verify this "
            "commitment applies to the specific tier in use."
        ),
    },
    "gemini": {
        "confidentiality": "cloud : data reuse possible",
        "confidentiality_note": (
            "Free tier via Google AI Studio: prompts and responses may be "
            "used by Google to improve its models. A paid tier with a "
            "no-training guarantee exists but is out of scope for this "
            "zero-cost benchmark."
        ),
    },
    "huggingface": {
        "confidentiality": "cloud : shared inference infrastructure",
        "confidentiality_note": (
            "Open-source model weights (Llama 3.1), but execution happens "
            "on Hugging Face's shared inference servers, not on infrastructure "
            "controlled by the end user."
        ),
    },
}
