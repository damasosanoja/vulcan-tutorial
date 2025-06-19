#!/usr/bin/env python3
from __future__ import annotations

import sys
import os
# Add the parent directory to Python's module search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ═══════════════════════════════════════════════════════════════════════════════
# Stage 2: Real AI Integration Runner (OpenAI + Gemini Support)
# ═══════════════════════════════════════════════════════════════════════════════
# This runner demonstrates Vulcan's production-ready hybrid approach using real
# LLM integration with flexible provider support. It showcases how the same
# hybrid architecture works identically with different AI providers while
# maintaining the exact same rule structure and business logic.

"""
Real AI Integration Runner for Tutorial Stage 2

This runner module demonstrates Vulcan's production AI capabilities with
comprehensive provider flexibility. It serves as the culmination of the
tutorial progression, showing how concepts from the mock simulation
translate seamlessly to real AI integration.

Key Architectural Demonstrations:
- Multi-provider support (OpenAI + Gemini) with identical interfaces
- Provider auto-detection prioritizing OpenAI (aligns with Vulcan ecosystem)
- Real microprompting methodology with production error handling
- Enhanced rules with deterministic fallback guardrails
- Seamless transition from mock to production AI

Provider Support Strategy:
- OpenAI: Primary provider (Vulcan's preferred integration)
- Gemini: Fallback provider (via OpenAI-compatible interface)
- Auto-detection: Tries OpenAI first, falls back to Gemini
- Manual selection: Via --provider flag for explicit control

Enhanced Rules Capability:
- Baseline rules: AI classification only
- Enhanced rules: AI + deterministic fallback safety nets
- Production patterns: Critical keywords override AI decisions
- Transparent operation: Clear logging when fallbacks engage

The runner maintains identical output format to the mock simulation,
enabling direct comparison and proving that Vulcan's hybrid architecture
enables seamless transition between development and production environments.

Usage Examples:
    # Auto-detect provider (prefers OpenAI)
    python runners/ai_integration.py events/event-1.txt
    
    # Explicit provider selection
    python runners/ai_integration.py --provider openai events/event-1.txt
    python runners/ai_integration.py --provider gemini events/event-1.txt
    
    # Enhanced rules with fallback guardrails
    python runners/ai_integration.py --provider openai --enhanced-rules events/event-4.txt
"""

import argparse
import importlib
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
# Multi-Provider LLM Configuration Engine
# ═══════════════════════════════════════════════════════════════════════════════
# This section demonstrates Vulcan's flexible AI integration approach: the same
# hybrid architecture works with any LLM provider while maintaining identical
# rule structures and business logic throughout the tutorial.

def make_llm(provider: str = "auto") -> ChatOpenAI:
    """
    Creates a production-configured LLM instance with multi-provider support.
    
    This function demonstrates several key production AI integration patterns:
    
    1. **Provider Flexibility**: Same interface works with OpenAI or Gemini
    2. **Auto-Detection Strategy**: Prioritizes OpenAI (aligns with Vulcan ecosystem)
    3. **Environment-Based Configuration**: Secure credential management
    4. **Production Settings**: Conservative parameters for business reliability
    5. **Clear Error Handling**: Actionable messages for missing credentials
    
    Provider Selection Logic:
    - "auto": Try OpenAI first, fallback to Gemini
    - "openai": Use OpenAI exclusively (requires OPENAI_API_KEY)
    - "gemini": Use Gemini exclusively (requires GEMINI_API_KEY)
    
    This flexibility enables organizations to:
    - Start development with one provider, switch to another in production
    - Use different providers for different cost/performance requirements
    - Maintain provider independence in their automation systems
    
    Tutorial Learning Points:
    - Hybrid architecture is provider-agnostic
    - Business logic remains unchanged across providers
    - Vulcan's microprompting works with any ChatModel-compatible LLM
    - Environment-based configuration enables secure deployment patterns
    
    Args:
        provider: Provider selection ("auto", "openai", "gemini")
        
    Returns:
        Configured ChatOpenAI instance ready for Vulcan integration
        
    Raises:
        RuntimeError: When no valid API keys are found for the requested provider
    """
    # ═══ Provider-Specific Configuration ═══
    if provider == "openai" or (provider == "auto" and os.getenv("OPENAI_API_KEY")):
        # OpenAI Configuration (Vulcan's preferred integration)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY not found. Set it as an environment variable or Codespace secret.\n"
                "Get your API key at: https://platform.openai.com/api-keys"
            )
        
        print("🤖 Using OpenAI integration (Vulcan's preferred provider)")
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=api_key,
            # Standard OpenAI endpoint (no base_url override needed)
            temperature=0,      # Maximum consistency for business decisions
            max_tokens=80,      # Focused responses for microprompting
        )
    
    elif provider == "gemini" or (provider == "auto" and os.getenv("GEMINI_API_KEY")):
        # Gemini Configuration (via OpenAI-compatible interface)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not found. Set it as an environment variable or Codespace secret.\n"
                "Get your API key at: https://aistudio.google.com/app/apikey"
            )
        
        print("🤖 Using Gemini integration (via OpenAI-compatible interface)")
        return ChatOpenAI(
            model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            temperature=0,      # Maximum consistency for business decisions
            max_tokens=80,      # Focused responses for microprompting
        )
    
    else:
        # No valid API keys found
        raise RuntimeError(
            "No AI provider API keys found. Set either:\n"
            "  OPENAI_API_KEY for OpenAI models (preferred), or\n"
            "  GEMINI_API_KEY for Gemini models (alternative)\n\n"
            "💡 Tip: Try the mock simulation first: ./demo 1"
        )

# ═══════════════════════════════════════════════════════════════════════════════
# Production AI-Enhanced Scenario Execution Engine
# ═══════════════════════════════════════════════════════════════════════════════
# This function orchestrates the complete production AI workflow while maintaining
# identical interfaces to the mock simulation, proving Vulcan's architectural
# consistency across development and production environments.

def run_scenario(event_file: str, provider: str = "auto", use_enhanced: bool = False) -> None:
    """
    Executes the complete production AI-enhanced supply chain risk assessment workflow.
    
    This function represents the culmination of the tutorial progression: a production-ready
    system that combines real AI intelligence with computational reliability. It demonstrates
    several critical production patterns:
    
    1. **Identical Interface**: Same function signature as mock simulation
    2. **Provider Flexibility**: Works with OpenAI, Gemini, or auto-detection
    3. **Enhanced Rules Option**: Adds deterministic fallback guardrails
    4. **Production Error Handling**: Comprehensive validation and clear error messages
    5. **Transparent Operation**: Complete audit trail with decision explanations
    
    Architecture Benefits Demonstrated:
    - Hybrid AI reasoning scales from development to production seamlessly
    - Business logic remains unchanged regardless of AI provider choice
    - Enhanced rules add safety nets without changing core rule structures
    - Forward-chaining creates intelligent automation workflows automatically
    
    Tutorial Learning Progression:
    - Stage 0: Pure deterministic rules (computational logic only)
    - Stage 1: Mock AI simulation (concept introduction without API complexity)
    - Stage 2: Real AI integration (production-ready hybrid automation)
    
    The enhanced rules option demonstrates Vulcan's key production advantage:
    critical business scenarios can be protected by deterministic guardrails
    that override AI decisions when necessary, ensuring business continuity
    regardless of AI performance variability.
    
    Args:
        event_file: Path to the news bulletin that will trigger risk assessment
        provider: AI provider selection ("auto", "openai", "gemini")
        use_enhanced: Whether to enable deterministic fallback guardrails
    """
    print(f"--- Running AI-Enhanced Scenario for Event: {event_file} ---")
    if use_enhanced:
        print("🛡️  Enhanced rules enabled (with deterministic fallback guardrails)")
    print()

    # ═══ Environment and Model Initialization ═══
    # Load environment configuration for secure credential management
    load_dotenv()
    engine = RuleEngine()
    llm = make_llm(provider)

    # ═══ Dynamic Rule System Selection ═══
    # This demonstrates Vulcan's modularity: different rule sets can be loaded
    # without changing the execution engine, workflow, or business logic
    # Updated to use the new provider-agnostic naming convention
    module_name = (
        "supply_chain.rules_ai_enhanced"
        if use_enhanced
        else "supply_chain.rules_ai_baseline"
    )
    
    print(f"📋 Loading rule set: {module_name.split('.')[-1]}")
    rules_mod = importlib.import_module(module_name)
    rules_mod.define_rules(engine, llm)

    # ═══ Knowledge Base Initialization ═══  
    # Establish the supply chain's baseline state before processing events
    # This represents "what we know before today's news affects our decisions"
    print("📊 Loading initial supply chain state...")
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
        print(f"❌ Error: Event file not found at {event_file}")
        print("📁 Available events: events/event-1.txt, events/event-2.txt, events/event-3.txt, events/event-4.txt")
        return

    engine.fact(NewsBulletin(content=content, region="Eastern Corridor"))
    print("📰 Loaded event trigger.\n")

    # ═══ AI-Enhanced Rule Evaluation ═══
    # Watch for the microprompt questions that demonstrate AI reasoning process
    # This shows how Vulcan breaks complex decisions into manageable AI tasks
    print("--- Evaluating AI-Enhanced Rules ---")
    engine.evaluate()
    print("--- Evaluation Complete ---\n")

    # ═══ Decision Analysis and Audit Trail ═══
    # Examine the results of our hybrid AI + deterministic decision system
    print("📢 Generated Alerts:")
    alerts = [f for f in engine.facts.values() if isinstance(f, Alert)]
    if alerts:
        for a in alerts:
            print(f"  - {a.message}")
    else:
        print("  - No alerts generated.")

    # Display the final business decision made by our hybrid system
    active = engine[ActiveSupplier]
    print(f"\n🏭 Active supplier: {active.supplier_name} ({active.supplier_region})")
    print("\n--- Scenario Complete ---")
    
    # ═══ Learning Summary ═══
    # Provide educational context about what was demonstrated
    print(f"\n💡 This demonstration showed:")
    print(f"   • Real AI classification using {provider} provider")
    print(f"   • Microprompting approach with three focused questions")
    print(f"   • Deterministic business logic triggered by AI decisions")
    if use_enhanced:
        print(f"   • Enhanced fallback rules for critical business scenarios")
    print(f"   • Complete audit trail for explainable automation")

# ═══════════════════════════════════════════════════════════════════════════════
# Command Line Interface for Production AI Testing
# ═══════════════════════════════════════════════════════════════════════════════
# This interface enables comprehensive testing of production AI integration with
# flexible provider selection and enhanced rule capabilities.

if __name__ == "__main__":
    """
    Command-line interface for AI integration testing and demonstration.
    
    This interface supports the complete tutorial learning progression by providing:
    - Multiple AI provider support for ecosystem flexibility
    - Enhanced rules option for production pattern demonstration
    - Clear error handling for missing credentials or files
    - Educational feedback about what features are being demonstrated
    
    The interface design prioritizes learning and experimentation:
    - Auto-detection enables immediate usage when credentials are available
    - Manual provider selection allows testing different AI ecosystems
    - Enhanced rules demonstrate production safety patterns
    - Clear error messages guide users toward successful execution
    
    Usage Patterns:
    - Quick testing: Just specify event file, let auto-detection handle provider
    - Provider comparison: Test same scenario with different AI providers
    - Production patterns: Use enhanced rules to see fallback guardrails
    - Error handling: Clear guidance when credentials or files are missing
    """
    parser = argparse.ArgumentParser(
        prog="ai_integration",
        description="AI-enhanced supply chain automation with multi-provider support",
        epilog="Examples: python runners/ai_integration.py events/event-1.txt --provider openai --enhanced-rules"
    )
    
    # Event file is required - this is the trigger data for our risk assessment
    parser.add_argument(
        "event_file", 
        help="Path to event trigger file (e.g., events/event-1.txt)"
    )
    
    # Provider selection with auto-detection default
    parser.add_argument(
        "--provider",
        choices=["auto", "openai", "gemini"],
        default="auto",
        help="AI provider selection: auto (detect), openai (explicit), gemini (explicit)"
    )
    
    # Enhanced rules for production patterns
    parser.add_argument(
        "--enhanced-rules",
        action="store_true",
        help="Enable enhanced rules with deterministic fallback guardrails for critical scenarios"
    )
    
    args = parser.parse_args()
    
    # Execute the AI-enhanced supply chain risk assessment
    run_scenario(args.event_file, args.provider, args.enhanced_rules)
