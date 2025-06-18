#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# Unified Tutorial Launcher Script
# ═══════════════════════════════════════════════════════════════════════════════
# This script provides a single, user-friendly entry point for all tutorial stages.
# It demonstrates best practices for command-line tool design: simple interface,
# clear options, and seamless delegation to the appropriate underlying implementation.
# This approach enables non-technical users to explore Vulcan concepts without
# needing to understand the internal project structure.

"""
Supply Chain Tutorial Launcher

This utility script provides a unified interface for running all three stages of
the Vulcan tutorial progression. It serves multiple important purposes:

Educational Benefits:
- Single command interface reduces cognitive load for tutorial readers
- Clear stage selection helps users understand the progression path
- Consistent usage pattern across all tutorial stages

Technical Benefits:  
- Delegates to appropriate underlying implementation without duplication
- Maintains clean separation between launcher logic and tutorial logic
- Enables easy integration with build systems and CI/CD pipelines

Usage Examples:
    # Stage 1: Mock AI simulation (no API key required)
    python supply_chain.py --mock events/event-1.txt
    
    # Stage 2: Real AI with baseline rules (requires GEMINI_API_KEY)
    python supply_chain.py events/event-1.txt
    
    # Stage 2: Real AI with enhanced fallback rules
    python supply_chain.py --enhanced events/event-1.txt

The launcher automatically determines which underlying runner to execute based
on the provided flags, making the tutorial experience seamless for users.
"""

import argparse
import subprocess
import sys

# ═══════════════════════════════════════════════════════════════════════════════
# Stage Mapping Configuration
# ═══════════════════════════════════════════════════════════════════════════════
# This mapping defines the relationship between user-friendly options and
# the actual implementation files. This indirection enables us to refactor
# internal structure without breaking the user-facing interface.

RUNNERS = {
    "mock":      ("python3", "main-01.py"),           # Stage 1: Mock AI simulation
    "gemini":    ("python3", "main-02.py"),           # Stage 2: Real AI baseline  
    "enhanced":  ("python3", "main-02.py", "--enhanced-rules"), # Stage 2: AI + fallbacks
}

# ═══════════════════════════════════════════════════════════════════════════════
# Command Line Interface Definition
# ═══════════════════════════════════════════════════════════════════════════════
# This interface demonstrates best practices for tutorial tooling: mutually
# exclusive options prevent user confusion, clear help text explains purpose,
# and sensible defaults minimize required knowledge.

def main():
    """
    Provides the unified command-line interface for all tutorial stages.
    
    This function demonstrates several CLI design principles important for
    educational tools:
    
    1. Mutually Exclusive Groups: Prevents invalid combinations that would confuse users
    2. Sensible Defaults: Baseline Gemini implementation is the "main" tutorial experience  
    3. Clear Documentation: Help text explains what each option demonstrates
    4. Direct Delegation: No business logic here, just interface translation
    
    The design enables users to focus on learning Vulcan concepts rather than
    wrestling with command-line complexity or project structure details.
    """
    # Create the main parser with clear program description
    parser = argparse.ArgumentParser(
        prog="supply_chain",
        description="Unified launcher for Vulcan supply chain tutorial stages"
    )
    
    # Event file is required for all stages - this is the trigger data
    parser.add_argument(
        "event_file", 
        help="Path to event trigger file (e.g., events/event-1.txt)"
    )
    
    # Create mutually exclusive group for stage selection
    # This prevents users from accidentally combining incompatible options
    stage = parser.add_mutually_exclusive_group()
    stage.add_argument(
        "--mock", 
        action="store_true",
        help="Run Stage 1: Mock AI simulation (no API key required)"
    )
    stage.add_argument(
        "--enhanced", 
        action="store_true", 
        help="Run Stage 2 Enhanced: Real AI with deterministic fallback guardrails"
    )
    
    # Default behavior (no stage flags) runs baseline Gemini implementation
    # This represents the core tutorial experience that most users should see
    
    args = parser.parse_args()

    # ═══ Stage Selection Logic ═══
    # Translate user-friendly options into internal runner selection
    # The default case (baseline Gemini) requires no explicit flag
    if args.mock:
        runner_key = "mock"
    elif args.enhanced:
        runner_key = "enhanced"
    else:
        runner_key = "gemini"  # Default: baseline real AI implementation

    # ═══ Command Construction and Execution ═══
    # Build the complete command by combining the runner specification
    # with the user-provided event file argument
    command_parts = list(RUNNERS[runner_key]) + [args.event_file]
    
    # Execute the appropriate underlying implementation and preserve its exit code
    # This ensures that any errors from the underlying runners are properly
    # propagated to the user and any automated systems (CI/CD, etc.)
    sys.exit(subprocess.call(command_parts))

if __name__ == "__main__":
    main()
