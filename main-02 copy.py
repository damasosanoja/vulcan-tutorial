# main-02.py
"""
REAL AI VERSION — GEMINI
------------------------
Runs the same supply-chain scenario as main.py but evaluates the
risk-detection rules with Gemini 2.x models via the OpenAI-compatible
endpoint.

Prerequisites
-------------
1. `pip install vulcan-core langchain-openai python-dotenv`
   (already in requirements.txt)
2. Add `GEMINI_API_KEY` to your `.env` or shell environment.

Usage
-----
$ python3 main-02.py events/event-1.txt
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from vulcan_core import RuleEngine

from supply_chain.initial_state import (
    INITIAL_SUPPLIER,
    BACKUP_SUPPLIER,
    INITIAL_ACTIVE_SUPPLIER,
    INITIAL_REGION_RISK_EASTERN,
    INITIAL_REGION_RISK_WESTERN,
)
from supply_chain.schema import Alert, ActiveSupplier, NewsBulletin
#from supply_chain import rules_gemini
from supply_chain import rules_gemini_enhanced



# --------------------------------------------------------------------------- #
# 1. Construct a Gemini-backed LangChain model                                #
# --------------------------------------------------------------------------- #
def make_llm() -> ChatOpenAI:
    """
    Returns a ChatOpenAI object configured for Gemini’s OpenAI-compatible
    endpoint.  Raises if GEMINI_API_KEY is missing.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is missing. "
            "Add it to .env or export it in your shell."
        )

    return ChatOpenAI(
        model="gemini-2.0-flash",  # pick any compatible Gemini chat model
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        temperature=0,
        max_tokens=80,
    )


# --------------------------------------------------------------------------- #
# 2. Scenario runner (mirrors main.py CLI)                                    #
# --------------------------------------------------------------------------- #
def run_scenario(event_file: str) -> None:
    print(f"--- Running Gemini Scenario for Event: {event_file} ---\n")

    load_dotenv()
    engine = RuleEngine()
    llm = make_llm()

    # Register AI-enabled rules
    #rules_gemini.define_rules(engine, llm)
    rules_gemini_enhanced.define_rules(engine, llm)

    # Seed initial working-memory state
    print("Loading initial state...")
    for fact in (
        INITIAL_SUPPLIER,
        BACKUP_SUPPLIER,
        INITIAL_ACTIVE_SUPPLIER,
        INITIAL_REGION_RISK_EASTERN,
        INITIAL_REGION_RISK_WESTERN,
    ):
        engine.fact(fact)

    # Insert the NewsBulletin trigger
    try:
        content = Path(event_file).read_text()
    except FileNotFoundError:
        print(f"Error: Event file not found at {event_file}")
        return

    engine.fact(NewsBulletin(content=content, region="Eastern Corridor"))
    print("Loaded event trigger.\n")

    # Evaluate rules
    print("--- Evaluating Rules ---")
    engine.evaluate()
    print("--- Evaluation Complete ---\n")

    # Show alerts
    print("Generated Alerts:")
    alerts = [f for f in engine.facts.values() if isinstance(f, Alert)]
    if alerts:
        for a in alerts:
            print(f"  - {a.message}")
    else:
        print("  - No alerts generated.")

    # Show current active supplier
    active = engine[ActiveSupplier]
    print(f"\nActive supplier is: {active.supplier_name}, ({active.supplier_region})")
    print("\n--- Scenario Complete ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Gemini supply-chain scenario.")
    parser.add_argument("event_file", type=str, help="Path to the event trigger file.")
    run_scenario(parser.parse_args().event_file)
