# ═══════════════════════════════════════════════════════════════════════════════
# Stage 1: Mock AI Integration Demo
# ═══════════════════════════════════════════════════════════════════════════════
# This module demonstrates Vulcan's hybrid concept using simulated AI reasoning.
# It bridges the gap between pure deterministic rules and real AI integration,
# showing how microprompting works without requiring API keys or handling
# the variability of real LLM responses.

"""
Mock AI Rules Module for Tutorial Stage 1

This module serves a critical pedagogical purpose in the Vulcan tutorial progression:
it demonstrates the exact same rule structure and output format as the real AI system
while using deterministic logic. This allows readers to:

- Understand AI integration concepts without API complexity
- Compare outputs directly with the real AI implementation  
- See how microprompting breaks complex decisions into focused questions
- Learn Vulcan's hybrid architecture in a controlled environment

Key Learning Demonstrations:
- Microprompting methodology through three sequential questions
- Deterministic simulation of AI-style reasoning
- Identical interfaces between mock and production AI systems
- Console output that matches real AI implementation exactly

The mock system uses keyword-based heuristics to simulate what an AI would decide,
providing predictable results that help readers understand the underlying concepts
before adding the complexity of real LLM integration.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from vulcan_core import RuleEngine, condition, action
from supply_chain.schema import (
    Supplier,
    NewsBulletin,
    RegionRisk,
    ActiveSupplier,
    Alert,
)

# ═══════════════════════════════════════════════════════════════════════════════
# Mock AI Decision Engine
# ═══════════════════════════════════════════════════════════════════════════════
# This section demonstrates Vulcan's microprompting approach using deterministic
# logic that simulates AI reasoning patterns. The three-question sequence mirrors
# exactly what the real AI implementation produces.

@lru_cache(maxsize=None)
def _analyze_risk_level(content: str, region: str) -> Literal["LOW", "MEDIUM", "HIGH"]:
    """
    Simulates AI-powered risk analysis through microprompting methodology.
    
    This function demonstrates Vulcan's key insight: complex AI decisions should be
    broken down into focused, answerable questions rather than overwhelming the AI
    with complex instructions. The three microprompts represent:
    
    1. Binary classification: Is there any risk present?
    2. Severity assessment: How serious is the identified risk?
    3. Scope validation: Does this risk affect our specific region?
    
    By using deterministic keyword matching, this mock produces the same decision
    logic an AI would follow, but with guaranteed consistency for tutorial purposes.
    This allows readers to understand the microprompting concept before adding
    the complexity of real LLM variability.
    
    Tutorial Value:
    - Shows how to break complex decisions into simple questions
    - Demonstrates consistent output format for comparison with real AI
    - Proves that AI integration doesn't require abandoning deterministic logic
    - Illustrates how hybrid systems combine predictability with intelligence
    """
    # Define risk classification criteria using business-relevant keywords
    # These simulate what an AI would recognize as indicators of different risk levels
    risk_keywords_high = ("tariff", "embargo", "sanction")
    risk_keywords_med = ("delay", "delays", "shortage", "congestion")
    
    content_lc = content.lower()

    # ═══ Microprompt 1: Risk Detection ═══
    # Simulate AI's ability to detect supply chain risks in natural language
    has_risk = any(k in content_lc for k in risk_keywords_high + risk_keywords_med)
    print("\n[MICROPROMPT 1] Does the bulletin indicate supply-chain risk?")
    print(f"  → {'YES' if has_risk else 'NO'}")

    # Early termination for no-risk scenarios (common AI pattern)
    if not has_risk:
        print("[MICROPROMPT 2] What is the *severity* of that risk?")
        print("  → LOW")
        print(f"[MICROPROMPT 3] Is the risk specific to {region}?")
        print("  → YES\n")
        return "LOW"

    # ═══ Microprompt 2: Severity Classification ═══
    # Demonstrate how AI categorizes risk levels based on business impact
    if any(k in content_lc for k in risk_keywords_high):
        severity = "HIGH"
    else:
        severity = "MEDIUM"
    print("[MICROPROMPT 2] What is the *severity* of that risk?")
    print(f"  → {severity}")

    # ═══ Microprompt 3: Regional Scope Validation ═══
    # Show how AI validates that risks apply to our specific operational area
    # In this mock, we always return YES to demonstrate the positive case
    print(f"[MICROPROMPT 3] Is the risk specific to {region}?")
    print("  → YES\n")

    return severity

# ═══════════════════════════════════════════════════════════════════════════════
# Rule Cascade Definition
# ═══════════════════════════════════════════════════════════════════════════════
# These rules demonstrate Vulcan's hybrid architecture: AI provides intelligent
# classification while deterministic rules handle the business logic cascade.
# This separation of concerns is key to reliable automated decision making.

def define_rules(engine: RuleEngine) -> None:
    """
    Demonstrates Vulcan's hybrid rule cascade using simulated AI classification.
    
    This function showcases the same five-rule cascade as the real AI implementation
    but uses our mock classifier instead of Gemini. This demonstrates several
    critical Vulcan concepts:
    
    1. AI Integration Point: Only the classification step uses "AI" reasoning
    2. Deterministic Cascade: All business logic remains computational  
    3. Identical Interfaces: Mock and real AI systems are interchangeable
    4. Separation of Concerns: AI handles recognition, rules handle logic
    
    The identical structure to the real AI system proves that Vulcan's hybrid
    approach allows reliable development and testing with deterministic behavior,
    then seamless transition to AI-enhanced production systems.
    """

    # ═══ Rule 1: AI-Enhanced Risk Classification ═══
    # This rule demonstrates how Vulcan integrates AI reasoning into rule cascades
    # The mock classifier simulates intelligent content analysis while providing
    # deterministic results for tutorial reliability
    engine.rule(
        name="mock_classify_region_risk",
        when=condition(lambda: bool(NewsBulletin.content)),
        then=action(
            lambda: RegionRisk(
                region=NewsBulletin.region,
                level=_analyze_risk_level(
                    NewsBulletin.content, NewsBulletin.region
                ),
            )
        ),
    )

    # ═══ Rule 2: Intelligent Supplier Switching Logic ═══
    # This rule demonstrates how AI classification triggers deterministic business logic
    # The conditions combine to create sophisticated decision making from simple components
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

    # ═══ Rule 3: Automated Alert Generation ═══
    # This rule shows how Vulcan's forward chaining creates intelligent workflows
    # When Rule 2 changes the supplier, this rule automatically fires to notify stakeholders
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

    # ═══ Rule 4: Risk Level Monitoring ═══
    # This rule demonstrates different response strategies for different AI classifications
    # MEDIUM risk generates monitoring alerts without triggering supplier changes
    engine.rule(
        name="alert_on_medium_risk",
        when=condition(lambda: RegionRisk.level == "MEDIUM"),
        then=action(
            lambda: Alert(
                message=f"ALERT: The risk in {RegionRisk.region} has changed to MEDIUM"
            )
        ),
    )
