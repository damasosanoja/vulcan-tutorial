#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# Stage 2: Real AI Integration Demo
# ═══════════════════════════════════════════════════════════════════════════════
# This file demonstrates Vulcan's production-ready hybrid approach using real
# Gemini LLM integration. It shows how to seamlessly transition from mock AI
# to production AI while maintaining identical workflow and output format.
# This stage proves Vulcan's core value: reliable AI-enhanced decision making.

"""
main-02.py – Tutorial stage-2 runner (real Gemini integration)

This stage demonstrates Vulcan's production AI capabilities while maintaining
the exact same rule structure and output format as the mock implementation.
Key demonstrations:

- Real LLM integration with proper API handling
- Identical microprompting approach to mock version  
- Optional enhanced rules with deterministic fallbacks
- Production-ready error handling and configuration

The ability to switch between mock and real AI with identical interfaces
showcases Vulcan's hybrid architecture advantage: you can develop and test
with deterministic behavior, then deploy with real AI confidence.

Usage Examples:
$ python3 main-02.py events/event-1.txt                    # baseline AI rules
$ python3 main-02.py events/event-4.txt --enhanced-rules   # with fallback guards
"""

from __future__ import annotations

import argparse
import importlib
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

# ═══════════════════════════════════════════════════════════════════════════════
# LLM Configuration and Setup
# ═══════════════════════════════════════════════════════════════════════════════
# This section shows how Vulcan integrates with production LLM services.
# The configuration demonstrates best practices for reliability and cost control.

def make_llm() -> ChatOpenAI:
    """
    Creates a production-configured Gemini model via OpenAI-compatible API.
    
    This function demonstrates Vulcan's LLM integration approach:
    - Environment-based configuration for security
    - Conservative temperature settings for consistency  
    - Token limits to control costs and focus responses
    - Clear error handling for missing credentials
    
    The choice of gemini-2.0-flash balances performance with cost,
    ideal for microprompting where response brevity is valued.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Add it to .env or export it in your shell."
        )

    return ChatOpenAI(
        model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        temperature=0,      # Maximum consistency for business decisions
        max_tokens=80,      # Focused responses for microprompting
    )

# ═══════════════════════════════════════════════════════════════════════════════
# Scenario Execution Engine  
# ═══════════════════════════════════════════════════════════════════════════════
# This section demonstrates Vulcan's modular rule system architecture.
# Notice how rule selection happens at runtime without changing core logic.

def run_scenario(event_file: str, use_enhanced: bool) -> None:
    """
    Executes the complete AI-enhanced supply chain risk assessment workflow.
    
    This function showcases Vulcan's key architectural benefits:
    1. Dynamic rule selection (baseline vs enhanced) without code duplication
    2. Identical workflow regardless of rule complexity
    3. Clear separation between AI reasoning and deterministic logic
    4. Transparent decision audit trail
    
    The enhanced rules option demonstrates Vulcan's hybrid approach:
    AI provides intelligent classification, while deterministic rules
    provide guardrails for critical business scenarios.
    """
    print(f"--- Running Gemini Scenario for Event: {event_file} ---\n")

    # ═══ Environment and Model Initialization ═══
    load_dotenv()
    engine = RuleEngine()
    llm = make_llm()

    # ═══ Dynamic Rule System Selection ═══
    # This demonstrates Vulcan's modularity: different rule sets can be
    # loaded without changing the execution engine or workflow
    module_name = (
        "supply_chain.rules_gemini_enhanced"
        if use_enhanced
        else "supply_chain.rules_gemini"
    )
    rules_mod = importlib.import_module(module_name)
    rules_mod.define_rules(engine, llm)

    # ═══ Knowledge Base Initialization ═══  
    # Establish the supply chain's baseline state before processing events
    # This represents "what we know before today's news affects our decisions"
    print("Loading initial state...")
    for fact in (
        INITIAL_SUPPLIER,
        BACKUP_SUPPLIER,
        INITIAL_ACTIVE_SUPPLIER,
        INITIAL_REGION_RISK_EASTERN,
        INITIAL_REGION_RISK_WESTERN,
    ):
        engine.fact(fact)

    # ═══ External Event Integration ═══
    # Load the trigger event that will test our AI-enhanced decision system
    # This simulates real-world information feeds affecting business decisions
    try:
        content = Path(event_file).read_text()
    except FileNotFoundError:
        print(f"Error: Event file not found at {event_file}")
        return

    engine.fact(NewsBulletin(content=content, region="Eastern Corridor"))
    print("Loaded event trigger.\n")

    # ═══ AI-Enhanced Rule Evaluation ═══
    # Watch for the microprompt questions that demonstrate AI reasoning process
    # This shows how Vulcan breaks complex decisions into manageable AI tasks
    print("--- Evaluating Rules ---")
    engine.evaluate()
    print("--- Evaluation Complete ---\n")

    # ═══ Decision Analysis and Audit Trail ═══
    # Examine the results of our hybrid AI + deterministic decision system
    print("Generated Alerts:")
    alerts = [f for f in engine.facts.values() if isinstance(f, Alert)]
    if alerts:
        for a in alerts:
            print(f"  - {a.message}")
    else:
        print("  - No alerts generated.")

    # Display the final business decision made by our hybrid system
    active = engine[ActiveSupplier]
    print(f"\nActive supplier is: {active.supplier_name}, ({active.supplier_region})")
    print("\n--- Scenario Complete ---")

# ═══════════════════════════════════════════════════════════════════════════════
# Command Line Interface
# ═══════════════════════════════════════════════════════════════════════════════
# This interface demonstrates how to expose Vulcan's flexibility to end users
# while maintaining simplicity for different operational scenarios.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run Gemini supply-chain scenario with optional enhanced rules."
    )
    parser.add_argument("event_file", help="Path to the event trigger text file.")
    parser.add_argument(
        "--enhanced-rules",
        action="store_true",
        help="Use enhanced rules with deterministic fallback guardrails for critical scenarios.",
    )
    args = parser.parse_args()
    run_scenario(args.event_file, args.enhanced_rules)
