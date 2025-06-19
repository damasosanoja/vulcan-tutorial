#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# Simplified Tutorial Demo Launcher
# ═══════════════════════════════════════════════════════════════════════════════
# This script provides a simplified, user-friendly entry point for all tutorial stages.
# It demonstrates best practices for educational tool design: intuitive commands,
# numbered scenarios, and clear delegation to specialized implementation modules.
# This approach enables users to focus on learning Vulcan concepts with minimal
# cognitive overhead from command-line complexity.

"""
Vulcan Tutorial Demo Launcher

This utility script provides a simplified interface for running all stages of
the Vulcan tutorial progression using intuitive numbered scenarios. It serves
multiple important educational and technical purposes:

Educational Benefits:
- Numbered scenarios (1-4) eliminate need to remember file paths
- Simple command structure: `demo 1` instead of complex paths
- Mock simulation as default ensures immediate success for first-time users
- Clear progression mapping helps users understand tutorial flow
- Immediate feedback with command preview before execution

Technical Benefits:  
- Clean separation between user interface and implementation modules
- Organized runner modules in dedicated subdirectory structure
- Maintains backward compatibility while improving user experience
- Enables easy integration with automated testing and CI/CD pipelines
- Supports multiple AI providers (OpenAI + Gemini) with auto-detection

Architecture Philosophy:
- Default to mock simulation (zero setup friction for beginners)
- Explicit flags for AI providers (--gemini, --openai) when ready
- Enhanced rules available for production patterns (--enhanced)
- Provider auto-detection prioritizes OpenAI (aligns with Vulcan ecosystem)

Usage Examples:
    # Default - works immediately, perfect for first-time users
    demo 1
    
    # Real AI when ready to try LLM integration
    demo 1 --gemini            # Uses Gemini API
    demo 1 --openai            # Uses OpenAI API
    
    # Advanced usage with production safeguards
    demo 1 --gemini --enhanced # Adds deterministic fallback rules
    demo 4 --openai --enhanced # Enhanced rules demo with OpenAI

The launcher automatically maps scenario numbers to appropriate event files
and determines which specialized runner module to execute based on the provided
flags, making the tutorial experience seamless and intuitive for users.
"""

import argparse
import subprocess
import sys

# ═══════════════════════════════════════════════════════════════════════════════
# Scenario Mapping Configuration
# ═══════════════════════════════════════════════════════════════════════════════
# This mapping provides an intuitive numbered interface to the tutorial scenarios.
# Each number corresponds to a specific supply chain risk event that demonstrates
# different aspects of Vulcan's hybrid AI decision-making capabilities.

SCENARIOS = {
    1: "events/event-1.txt",  # HIGH risk - Tariff announcement triggers supplier switch
    2: "events/event-2.txt",  # LOW risk - Normal operations, no alerts generated  
    3: "events/event-3.txt",  # MEDIUM risk - Shipping delays create monitoring alerts
    4: "events/event-4.txt",  # Enhanced rules demo - Fallback logic demonstration
}

# ═══════════════════════════════════════════════════════════════════════════════
# Runner Module Configuration  
# ═══════════════════════════════════════════════════════════════════════════════
# This mapping defines the relationship between user-friendly options and
# the specialized implementation modules in the runners/ directory. The modular
# approach enables clean separation of concerns and easier maintenance.

RUNNER_CONFIGS = {
    "mock": {
        "command": ["python3", "runners/mock_simulation.py"],
        "description": "mock simulation"
    },
    "gemini": {
        "command": ["python3", "runners/ai_integration.py", "--provider", "gemini"],
        "description": "Gemini integration"
    },
    "openai": {
        "command": ["python3", "runners/ai_integration.py", "--provider", "openai"],
        "description": "OpenAI integration"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# Command Line Interface Definition
# ═══════════════════════════════════════════════════════════════════════════════
# This interface demonstrates best practices for educational tooling: simple
# numbered scenarios, mutually exclusive options, and immediate command feedback
# to help users understand what's happening behind the scenes.

def main():
    """
    Provides the simplified command-line interface for all tutorial stages.
    
    This function demonstrates several CLI design principles important for
    educational tools:
    
    1. Numbered Scenarios: Users specify 1-4 instead of remembering file paths
    2. Default to Mock: Zero-friction start for immediate learning success
    3. Explicit AI Providers: Clear flags when users are ready for real AI
    4. Mutually Exclusive Groups: Prevents invalid combinations that would confuse users
    5. Command Transparency: Shows users exactly what's being executed
    6. Clear Error Messages: Guides users when they provide invalid combinations
    
    The design enables users to focus on learning Vulcan concepts rather than
    wrestling with command-line complexity or internal project structure details.
    Educational progression: Mock → Gemini/OpenAI → Enhanced Rules
    """
    # Create the main parser with clear program description
    parser = argparse.ArgumentParser(
        prog="demo",
        description="Simplified launcher for Vulcan tutorial scenarios",
        epilog="Examples: demo 1 (mock), demo 1 --gemini (real AI), demo 1 --openai --enhanced (production patterns)"
    )
    
    # Scenario number is required - maps to specific supply chain events
    parser.add_argument(
        "scenario", 
        type=int,
        choices=SCENARIOS.keys(),
        help="Tutorial scenario number: 1=Tariff Crisis, 2=Normal Ops, 3=Delays, 4=Enhanced Demo"
    )
    
    # Create mutually exclusive group for AI provider selection
    # This prevents users from accidentally combining incompatible options
    provider_group = parser.add_mutually_exclusive_group()
    provider_group.add_argument(
        "--gemini", 
        action="store_true",
        help="Use Gemini AI integration (requires GEMINI_API_KEY)"
    )
    provider_group.add_argument(
        "--openai", 
        action="store_true",
        help="Use OpenAI integration (requires OPENAI_API_KEY)"
    )
    
    # Optional enhancement modifier (only valid with AI providers)
    parser.add_argument(
        "--enhanced", 
        action="store_true",
        help="Add deterministic fallback guardrails (only valid with --gemini or --openai)"
    )
    
    args = parser.parse_args()

    # ═══ Input Validation ═══
    # Provide clear error messages for invalid scenario numbers and flag combinations
    if args.scenario not in SCENARIOS:
        print(f"Error: Scenario {args.scenario} not found. Available scenarios: {list(SCENARIOS.keys())}")
        sys.exit(1)

    # Validation: enhanced requires an AI provider
    if args.enhanced and not (args.gemini or args.openai):
        parser.error("--enhanced requires either --gemini or --openai (enhanced rules don't apply to mock simulation)")

    # ═══ Runner Selection Logic ═══
    # Translate user-friendly options into internal runner module selection
    # Default case (no AI flags) uses mock simulation for immediate success
    if args.gemini:
        runner_key = "gemini"
        processing_mode = "Gemini integration"
    elif args.openai:
        runner_key = "openai"
        processing_mode = "OpenAI integration"
    else:
        # Default: Mock simulation (works immediately, no API key required)
        runner_key = "mock"
        processing_mode = "mock simulation"
        
        # Inform users about the educational progression if they used default
        if not any([args.gemini, args.openai]):
            print("💡 Using mock AI simulation (no API key required)")
            print("   Ready for real AI? Try: demo {} --gemini or demo {} --openai".format(args.scenario, args.scenario))
            print()

    # ═══ Command Construction and Execution ═══
    # Build the complete command by combining the runner specification
    # with the mapped event file for the selected scenario
    command_parts = RUNNER_CONFIGS[runner_key]["command"].copy()
    
    # Add enhanced rules flag if requested (only valid for AI providers)
    if args.enhanced and runner_key != "mock":
        command_parts.append("--enhanced-rules")
        processing_mode += " (enhanced)"
    
    # Add the event file for the selected scenario
    command_parts.append(SCENARIOS[args.scenario])
    
    # Provide transparency by showing users exactly what's being executed
    # This helps with learning and debugging while maintaining simplicity
    print(f"Running scenario {args.scenario} with {processing_mode}:")
    print(f"Command: {' '.join(command_parts)}")
    print()  # Add spacing for cleaner output
    
    # Execute the appropriate specialized runner module and preserve its exit code
    # This ensures that any errors from the underlying implementations are properly
    # propagated to the user and any automated systems (CI/CD, etc.)
    sys.exit(subprocess.call(command_parts))

if __name__ == "__main__":
    main()
