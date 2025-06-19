#!/usr/bin/env python3
from __future__ import annotations

import sys
import os
# Add the parent directory to Python's module search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ═══════════════════════════════════════════════════════════════════════════════
# Stage 1: Mock AI Simulation Runner
# ═══════════════════════════════════════════════════════════════════════════════
# This runner demonstrates Vulcan's hybrid approach using simulated AI decisions.
# It serves as a crucial bridge between pure deterministic rules (Stage 0) and 
# real AI integration (Stage 2), allowing learners to understand AI concepts
# without requiring API keys or dealing with LLM variability.

"""
Mock AI Simulation Runner for Tutorial Stage 1

This runner module serves a critical pedagogical purpose in the Vulcan tutorial 
progression. It demonstrates the exact same rule structure and output format as 
the real AI implementation while using deterministic logic, providing several 
key educational benefits:

Learning Progression Benefits:
- Introduces AI integration concepts without API complexity
- Demonstrates microprompting methodology through three sequential questions
- Shows identical console output to real AI implementation for direct comparison
- Proves that hybrid architecture works with both mock and production AI

Technical Architecture Demonstrations:
- Same rule cascade structure as production AI system
- Identical fact schema and business logic flow
- Forward-chaining automation that matches real AI behavior
- Clean separation between AI reasoning simulation and business rules

Practical Advantages:
- Zero configuration required - works immediately
- Consistent, reproducible results for tutorial exercises
- Perfect for offline learning and classroom environments
- Enables understanding of concepts before adding AI variability

The mock system uses keyword-based heuristics to simulate what an AI would 
decide, providing predictable results that help readers understand the 
underlying concepts before transitioning to real LLM integration.

Usage:
    python runners/mock_simulation.py events/event-1.txt
    
Expected Output:
    - Three microprompt questions showing AI reasoning process
    - Supply chain risk classification and decision cascade
    - Identical format to real AI implementation for easy comparison
"""

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

# ═══════════════════════════════════════════════════════════════════════════════
# Mock AI Simulation Execution Engine
# ═══════════════════════════════════════════════════════════════════════════════
# This function orchestrates the complete tutorial workflow using simulated AI
# reasoning. It demonstrates the same execution pattern as real AI integration
# while providing guaranteed consistency for educational purposes.

def run_scenario(event_file: str) -> None:
    """
    Executes the complete mock AI-enhanced supply chain risk assessment workflow.
    
    This function demonstrates Vulcan's hybrid architecture using deterministic 
    simulation of AI reasoning. It serves multiple educational purposes:
    
    1. **Concept Introduction**: Shows how AI integration works without API complexity
    2. **Output Consistency**: Provides identical console format to real AI system
    3. **Architecture Validation**: Proves the hybrid approach works with any intelligence source
    4. **Learning Confidence**: Builds understanding before adding real AI variability
    
    Tutorial Learning Points:
    - Same rule execution pattern as production AI systems
    - Microprompting approach broken into three clear questions
    - Forward-chaining automation creates intelligent decision cascades
    - Business logic separation from AI reasoning simulation
    
    The function follows the identical workflow as the real AI implementation:
    1. Initialize engine with mock AI-enhanced rules
    2. Load baseline supply chain state
    3. Process external event trigger
    4. Execute AI simulation and business logic cascade
    5. Analyze results and display decision audit trail
    
    This consistency enables direct comparison with real AI output and proves
    that Vulcan's architecture enables seamless transition between mock and
    production intelligence sources.
    """
    print(f"--- Running Mock Microprompt Scenario for Event: {event_file} ---\n")

    # ═══ Environment and Engine Setup ═══
    # Load environment configuration (though no API keys needed for mock simulation)
    # This maintains consistency with real AI implementation for easy transition
    load_dotenv()
    engine = RuleEngine()
    define_rules(engine)

    # ═══ Working Memory Initialization ═══
    # Establish the supply chain's baseline state before processing events
    # This represents "what we know before today's news affects our decisions"
    # The exact same initial state used by real AI implementation ensures identical starting conditions
    for fact in (
        INITIAL_SUPPLIER,
        BACKUP_SUPPLIER,
        INITIAL_ACTIVE_SUPPLIER,
        INITIAL_REGION_RISK_EASTERN,
        INITIAL_REGION_RISK_WESTERN,
    ):
        engine.fact(fact)

    # ═══ External Event Integration ═══
    # Load the trigger event that will test our mock AI reasoning system
    # This simulates real-world information feeds that affect business decisions
    try:
        content = Path(event_file).read_text()
    except FileNotFoundError:
        print(f"Error: Event file not found at {event_file}")
        return

    # Add the news bulletin to working memory as a triggering fact
    # This will activate our mock AI reasoning rules and demonstrate the decision cascade
    engine.fact(NewsBulletin(content=content, region="Eastern Corridor"))
    print("Loaded event trigger.\n")

    # ═══ Mock AI Rule Evaluation and Business Logic Cascade ═══
    # Watch the console output for the three microprompt questions
    # These demonstrate how complex AI decisions are broken into focused questions
    # The mock provides identical output format to real AI for direct comparison
    print("--- Evaluating Rules ---")
    engine.evaluate()
    print("--- Evaluation Complete ---\n")

    # ═══ Decision Analysis and Results ═══
    # Examine what decisions the mock AI reasoning system made
    # This demonstrates the complete audit trail and explainable decision process
    print("Generated Alerts:")
    alerts = [f for f in engine.facts.values() if isinstance(f, Alert)]
    if alerts:
        for a in alerts:
            print(f"  - {a.message}")
    else:
        print("  - No alerts generated.")

    # Display the final supplier decision made by our hybrid mock system
    # This shows the end result of combining simulated AI classification with deterministic business logic
    active = engine[ActiveSupplier]
    print(f"\nActive supplier is: {active.supplier_name}, ({active.supplier_region})")
    print("\n--- Scenario Complete ---")

# ═══════════════════════════════════════════════════════════════════════════════
# Command Line Interface for Educational Testing
# ═══════════════════════════════════════════════════════════════════════════════
# This interface enables students and instructors to easily test different scenarios
# and understand how mock AI reasoning responds to various supply chain events.

if __name__ == "__main__":
    """
    Command-line interface for mock AI simulation testing.
    
    This interface supports the educational goals of the tutorial by providing:
    - Simple command structure for testing different scenarios
    - Clear error handling for missing event files
    - Immediate feedback for learning and experimentation
    - Identical usage pattern to real AI implementation
    
    The mock simulation is perfect for:
    - Classroom demonstrations without API key requirements
    - Offline learning and development environments
    - Understanding concepts before adding real AI complexity
    - Comparing outputs directly with real AI implementation
    """
    parser = argparse.ArgumentParser(description="Run the mock Vulcan scenario.")
    parser.add_argument("event_file", type=str, help="Path to the event trigger file.")
    run_scenario(parser.parse_args().event_file)
