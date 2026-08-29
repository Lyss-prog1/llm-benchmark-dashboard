"""
prompts.py

Fixed set of test prompts used across all benchmark runs, one per enterprise
use case mirrored from Project 1 (Enterprise AI Assistant). Keeping this
separate from run_benchmark.py means the prompt set can grow or change
without touching the benchmark logic itself, and keeps every run comparable
against the same fixed inputs.
"""

PROMPTS = [
    {
        "use_case": "sales_assistant",
        "prompt": (
            "A prospect says: 'Your product looks similar to what we already use, "
            "why should we switch?' Write a concise objection-handling response "
            "a sales rep could use, in a confident but non-pushy tone."
        ),
    },
    {
        "use_case": "financial_due_diligence",
        "prompt": (
            "Summarize, in 3 bullet points, the kind of financial risks an analyst "
            "should look for when reviewing a fintech startup's annual report "
            "before an investment decision."
        ),
    },
    {
        "use_case": "hr_onboarding",
        "prompt": (
            "An employee asks: 'How many paid vacation days do I get in my first "
            "year?' Write a short, clear answer an HR onboarding assistant could "
            "give, assuming a standard French labor convention applies."
        ),
    },
]
