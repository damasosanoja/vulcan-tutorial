# ═══════════════════════════════════════════════════════════════════════════════
# Stage 0: Pure Deterministic Rules Demo
# ═══════════════════════════════════════════════════════════════════════════════
# This file demonstrates Vulcan's foundation: computational logic without AI.
# It shows how traditional rule engines work before we add AI enhancement.
# This creates the baseline for comparing with AI-powered stages.

import argparse
from dotenv import load_dotenv
from vulcan_core import RuleEngine

from supply_chain.initial_state import (
    INITIAL_SUPPLIER, 
    BACKUP_SUPPLIER, 
    INITIAL_ACTIVE_SUPPLIER,
    INITIAL_REGION_RISK_EASTERN,
    INITIAL_REGION_RISK_WESTERN
)
from supply_chain.rules import define_rules
from supply_chain.schema import NewsBulletin, Alert, ActiveSupplier

def run_scenario(event_file: str):
    """
    Demonstrates basic Vulcan workflow: Facts → Rules → Evaluation → Results.
    
    This function shows the core cycle that all Vulcan applications follow:
    1. Initialize engine and define rules
    2. Load initial facts (starting state)
    3. Add trigger event (new information)
    4. Evaluate rules (let Vulcan decide)
    5. Examine results (see what changed)
    """
    print(f"--- Running Simplified Scenario for Event: {event_file} ---\n")

    # ═══ Engine Initialization ═══
    # Load environment variables for any future API keys
    load_dotenv()
    engine = RuleEngine()
    define_rules(engine)

    # ═══ Initial Knowledge Base Setup ═══
    # These facts represent our supply chain's starting state
    # Think of this as "what we know before today's news"
    print("Loading initial state...")
    engine.fact(INITIAL_SUPPLIER)
    engine.fact(BACKUP_SUPPLIER)
    engine.fact(INITIAL_ACTIVE_SUPPLIER)
    engine.fact(INITIAL_REGION_RISK_EASTERN)
    engine.fact(INITIAL_REGION_RISK_WESTERN)
    
    # ═══ Event Trigger Processing ═══
    # Load external event that might change our decisions
    # This simulates real-world: news, alerts, data feeds, etc.
    try:
        with open(event_file, 'r') as f:
            content = f.read()
            bulletin = NewsBulletin(content=content, region="Eastern Corridor")
            engine.fact(bulletin)
            print("Loaded event trigger.")
    except FileNotFoundError:
        print(f"Error: Event file not found at {event_file}")
        return

    # ═══ Rule Evaluation ═══
    # Let Vulcan determine what actions to take based on all facts
    # Rules fire automatically when their conditions are met
    print("\n--- Evaluating Rules ---")
    engine.evaluate()
    print("--- Evaluation Complete ---\n")

    # ═══ Results Analysis ═══
    # Examine what decisions were made and why
    print("Generated Alerts:")
    alerts = [fact for fact in engine.facts.values() if isinstance(fact, Alert)]
    if alerts:
        for alert in alerts:
            print(f"  - {alert.message}")
    else:
        print("  - No alerts generated.")

    # Display final supplier decision using Vulcan's fact retrieval
    try:
        active_supplier = engine[ActiveSupplier]
        print(f"\nActive supplier is: {active_supplier.supplier_name}, ({active_supplier.supplier_region})")
    except KeyError:
        print("\nNo active supplier found in working memory.")

    print("\n--- Scenario Complete ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a supply chain risk scenario.")
    parser.add_argument("event_file", type=str, help="Path to the event trigger file.")
    args = parser.parse_args()
    run_scenario(args.event_file)
