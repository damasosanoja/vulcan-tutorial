# ═══════════════════════════════════════════════════════════════════════════════
# Stage 2: Real AI Integration Demo (Baseline)
# ═══════════════════════════════════════════════════════════════════════════════
# This module demonstrates Vulcan's production-ready hybrid approach using real
# Gemini LLM integration. It mirrors the mock implementation's structure and output
# format exactly, proving that Vulcan's architecture enables seamless transition
# from development to production AI systems without changing rule logic.

"""
Real AI Rules Module for Tutorial Stage 2 (Baseline)

This module represents the culmination of the tutorial progression: a production-ready
hybrid system that combines real AI intelligence with computational reliability.
Key demonstrations:

- Seamless transition from mock to real AI using identical interfaces
- Microprompting methodology applied to real LLM interactions
- Production error handling and response validation
- Identical console output format for direct comparison with mock system

Architecture Benefits Showcased:
- AI integration point clearly separated from business logic
- Deterministic rule cascade remains unchanged from earlier stages
- Forward-chaining creates intelligent automation workflows
- Hybrid approach combines AI flexibility with computational consistency

The microprompting approach used here demonstrates Vulcan's core insight:
complex AI tasks should be broken into focused, answerable questions rather
than overwhelming the AI with complex instructions. This reduces hallucination
risk while maintaining the explainability of decision processes.
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Tuple

from vulcan_core import RuleEngine, condition, action
from vulcan_core.actions import ActionReturn
from supply_chain.prompt_loader import load_prompt
from supply_chain.schema import (
    NewsBulletin,
    RegionRisk,
    Supplier,
    ActiveSupplier,
    Alert,
)

# ═══════════════════════════════════════════════════════════════════════════════
# Global LLM Configuration
# ═══════════════════════════════════════════════════════════════════════════════
# The LLM instance is stored globally to enable clean lambda expressions in rules.
# This pattern allows rule definitions to remain simple while ensuring the AI model
# is properly configured and shared across all rule evaluations.

_LLM = None  # Configured in define_rules() with production Gemini model


# ═══════════════════════════════════════════════════════════════════════════════
# AI-Powered Risk Classification Engine
# ═══════════════════════════════════════════════════════════════════════════════
# This section demonstrates Vulcan's microprompting approach using real AI.
# The three-question sequence showcases how complex business decisions can be
# broken down into focused, manageable AI tasks.

@lru_cache(maxsize=None)
def _ask_llm(bulletin: str, region: str) -> Tuple[bool, str, bool]:
    """
    Executes Vulcan's microprompting methodology using real Gemini LLM.
    
    This function demonstrates several critical production AI concepts:
    
    1. Microprompting Strategy: Complex risk assessment is broken into three
       focused questions that are easier for AI to answer reliably
    2. Caching: Results are cached to avoid redundant API calls for identical inputs
    3. Response Validation: AI responses are parsed and validated for expected format
    4. Error Handling: Clear exceptions for malformed AI responses
    
    The three microprompts represent a proven pattern for reliable AI integration:
    - Binary classification (yes/no) for initial screening
    - Severity assessment within constrained options
    - Scope validation for business relevance
    
    This approach significantly reduces AI hallucination risk compared to
    complex, multi-step instructions in a single prompt.
    
    Returns:
        Tuple of (has_risk: bool, severity: str, region_specific: bool)
        that drives the downstream business logic cascade.
    """
    # Load the structured prompt template for consistent AI interaction
    # Separating prompts from code enables easy iteration without code changes
    template = load_prompt("ai-reasoning-prompt.txt")
    prompt = template.format(bulletin=bulletin, region=region)

    # Execute the AI reasoning with production error handling
    reply = _LLM.invoke(prompt)  # type: ignore[attr-defined]
    
    # Parse and validate AI response using deterministic pattern matching
    # This hybrid approach combines AI intelligence with computational validation
    tokens = re.findall(r"(YES|NO|LOW|MEDIUM|HIGH)", reply.content.upper())
    if len(tokens) < 3:
        raise ValueError(f"Unexpected LLM reply: {reply.content!r}")

    return tokens[0] == "YES", tokens[1], tokens[2] == "YES"


# ═══════════════════════════════════════════════════════════════════════════════
# AI-Enhanced Action: Classification with Audit Trail
# ═══════════════════════════════════════════════════════════════════════════════
# This function combines AI reasoning with deterministic business logic while
# providing transparent decision audit trails for explainable automation.

def _classify_and_print(bulletin: NewsBulletin) -> ActionReturn:
    """
    Integrates AI classification with explainable decision audit trails.
    
    This function demonstrates Vulcan's hybrid value proposition:
    - AI provides intelligent content analysis
    - Deterministic logic handles business rule application
    - Console output provides complete decision transparency
    - Return format integrates seamlessly with rule cascade
    
    The printed microprompt questions serve multiple purposes:
    1. Educational: Shows readers how AI reasoning is structured
    2. Debugging: Provides insight into AI decision process
    3. Auditing: Creates log trail for business decision review
    4. Comparison: Enables direct output comparison with mock system
    
    This transparency is crucial for business-critical automation where
    decision justification and audit trails are required.
    """
    # Execute the three-step microprompting process with real AI
    has_risk, severity, region_specific = _ask_llm(bulletin.content, bulletin.region)

    # Provide complete decision audit trail through console output
    # This mirrors the mock system output exactly for easy comparison
    print("\n[MICROPROMPT 1] Does the bulletin indicate supply-chain risk?")
    print(f"  → {'YES' if has_risk else 'NO'}")
    print("[MICROPROMPT 2] What is the *severity* of that risk?")
    print(f"  → {severity}")
    print(f"[MICROPROMPT 3] Is the risk specific to {bulletin.region}?")
    print(f"  → {'YES' if region_specific else 'NO'}\n")

    # Apply deterministic business logic to AI classification results
    # This hybrid approach ensures reliable decision making
    final_level = severity if (has_risk and region_specific) else "LOW"
    return RegionRisk(region=bulletin.region, level=final_level)


# ═══════════════════════════════════════════════════════════════════════════════
# Production Rule Cascade Definition
# ═══════════════════════════════════════════════════════════════════════════════
# These rules demonstrate the complete Vulcan hybrid architecture: AI-enhanced
# classification triggers deterministic business logic cascades that create
# intelligent, explainable, and reliable automated decision systems.

def define_rules(engine: RuleEngine, llm) -> None:
    """
    Demonstrates Vulcan's complete hybrid architecture in production.
    
    This function showcases the identical rule structure to the mock implementation
    while using real AI for classification. Key architectural demonstrations:
    
    1. AI Integration Point: Only the classification rule uses AI reasoning
    2. Business Logic Separation: All downstream rules remain deterministic
    3. Interface Consistency: Identical structure enables mock-to-production transition
    4. Forward Chaining: AI classification automatically triggers business cascades
    
    The five-rule cascade represents a complete business automation workflow:
    - Rule 1: AI classifies risk level from natural language content
    - Rule 2: Deterministic supplier switching based on risk classification
    - Rule 3: Automated alert generation for critical supplier changes
    - Rule 4: Informational alerts for monitoring moderate risk levels
    
    This pattern proves Vulcan's core value: reliable AI-enhanced automation
    that combines intelligent classification with predictable business logic.
    """
    # Configure the global LLM instance for use in AI-enhanced rules
    global _LLM
    _LLM = llm

    # ═══ Rule 1: AI-Enhanced Risk Classification ═══
    # This rule demonstrates Vulcan's AI integration approach: focused,
    # reliable classification that feeds into deterministic business logic
    engine.rule(
        name="ai_classify_region_risk",
        when=condition(lambda: bool(NewsBulletin.content)),
        then=action(_classify_and_print),
    )

    # ═══ Rule 2: Intelligent Supplier Switching ═══
    # This rule showcases how AI classification results trigger sophisticated
    # business logic without requiring additional AI reasoning
    high_risk_active = condition(
        lambda: RegionRisk.level == "HIGH"
        and ActiveSupplier.supplier_region == RegionRisk.region
    )
    backup_available = condition(
        lambda: Supplier.region != ActiveSupplier.supplier_region
    )

    engine.rule(
        name="switch_supplier_on_high_risk",
        when=high_risk_active & backup_available,
        then=action(
            lambda: ActiveSupplier(
                supplier_name=Supplier.name,
                supplier_region=Supplier.region,
            )
        ),
    )

    # ═══ Rule 3: Critical Decision Alert System ═══
    # This rule demonstrates Vulcan's forward-chaining capability: when Rule 2
    # changes the supplier, this rule automatically fires to notify stakeholders
    engine.rule(
        name="alert_on_supplier_switch",
        when=condition(lambda: ActiveSupplier.supplier_region != "Eastern Corridor"),
        then=action(
            lambda: Alert(
                message=(
                    "CRITICAL ALERT: The new primary supplier is "
                    f"{ActiveSupplier.supplier_name}, "
                    f"({ActiveSupplier.supplier_region})"
                )
            )
        ),
    )

    # ═══ Rule 4: Risk Monitoring and Alerting ═══
    # This rule shows how the same AI classification can trigger different
    # business responses based on risk levels, enabling graduated responses
    engine.rule(
        name="alert_on_medium_risk",
        when=condition(lambda: RegionRisk.level == "MEDIUM"),
        then=action(
            lambda: Alert(
                message=f"ALERT: The risk in {RegionRisk.region} has changed to MEDIUM"
            )
        ),
    )
