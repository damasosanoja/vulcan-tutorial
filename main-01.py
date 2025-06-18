#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# Stage 1: Mock AI Integration Demo  
# ═══════════════════════════════════════════════════════════════════════════════
# This file demonstrates Vulcan's hybrid approach using simulated AI decisions.
# It shows how microprompting works without requiring API keys, providing
# a stepping stone between pure deterministic rules and real AI integration.
# The mock responses mirror exactly what the real Gemini integration produces.

"""
main-01.py – Tutorial stage-1 runner (mock microprompting)

This stage introduces the concept of AI-enhanced decision making within Vulcan
while remaining completely deterministic. It demonstrates:
- How Vulcan integrates AI-style reasoning into rule engines
- The three-step microprompting approach for risk assessment
- Console output that matches the real AI implementation for easy comparison

Key Learning Points:
- Microprompting breaks complex decisions into focused questions
- AI integration doesn't require abandoning deterministic behavior
- Vulcan enables seamless transition from mock to real AI

Usage
-----
$ python3 main-01.py events/event-1.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv
from vulcan_core import RuleEngine

from supply_chain.initial_state import (
    INITIAL_SUPPLIER,
    BACKUP_SUPPLIER,
    INITIAL_ACTIVE_SUPPLIER,
    INITIAL_REGION_RISK_EASTERN,
    INITIAL_REGION_RISK_WESTERN,
)
from supply_chain.rules_mock import define_rules
from supply_chain.schema import NewsBulletin, Alert, ActiveSupplier

def run_scenario(event_file: str) -> None:
    """
    Demonstrates Vulcan's mock AI integration workflow.
    
    This function shows how AI-enhanced rules work conceptually before
    adding the complexity of real LLM integration. The mock system:
    1. Processes the same inputs as the real AI system
    2. Uses deterministic logic to simulate AI reasoning
    3. Produces identical output format for comparison
    4. Demonstrates the microprompting question sequence
    
    This allows tutorial readers to understand the AI integration concept
    without needing API keys or dealing with potential AI variability.
    """
    print(f"--- Running Mock Microprompt Scenario for Event: {event_file} ---\n")

    # ═══ Environment and Engine Setup ═══
    # Load environment (though no API keys needed for mock)
    load_dotenv()
    engine = RuleEngine()
    define_rules(engine)

    # ═══ Working Memory Initialization ═══
    # Seed the knowledge base with our supply chain's starting state
    # This represents "what we know before processing today's events"
    for fact in (
        INITIAL_SUPPLIER,
        BACKUP_SUPPLIER,
        INITIAL_ACTIVE_SUPPLIER,
        INITIAL_REGION_RISK_EASTERN,
        INITIAL_REGION_RISK_WESTERN,
    ):
        engine.fact(fact)

    # ═══ Event Processing ═══
    # Load the external trigger event (news bulletin, alert, etc.)
    # This simulates real-world information flowing into our system
    try:
        content = Path(event_file).read_text()
    except FileNotFoundError:
        print(f"Error: Event file not found at {event_file}")
        return

    # Add the news bulletin to working memory as a new fact
    # This will trigger our mock AI reasoning rules
    engine.fact(NewsBulletin(content=content, region="Eastern Corridor"))
    print("Loaded event trigger.\n")

    # ═══ Rule Evaluation and AI Simulation ═══
    # Watch for the three microprompt questions in the output
    # These demonstrate how complex AI decisions are broken down
    print("--- Evaluating Rules ---")
    engine.evaluate()
    print("--- Evaluation Complete ---\n")

    # ═══ Results Analysis ═══
    # Examine what decisions the mock AI system made
    print("Generated Alerts:")
    alerts = [f for f in engine.facts.values() if isinstance(f, Alert)]
    if alerts:
        for a in alerts:
            print(f"  - {a.message}")
    else:
        print("  - No alerts generated.")

    # Display the final supplier decision
    # This shows the end result of our mock AI reasoning cascade
    active = engine[ActiveSupplier]
    print(f"\nActive supplier is: {active.supplier_name}, ({active.supplier_region})")
    print("\n--- Scenario Complete ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the mock Vulcan scenario.")
    parser.add_argument("event_file", type=str, help="Path to the event trigger file.")
    run_scenario(parser.parse_args().event_file)
