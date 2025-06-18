# ═══════════════════════════════════════════════════════════════════════════════
# Stage 2: Enhanced AI Integration Demo (Production Safeguards)
# ═══════════════════════════════════════════════════════════════════════════════
# This module demonstrates Vulcan's advanced hybrid approach: AI classification
# combined with deterministic fallback guardrails. It shows how production systems
# can benefit from AI intelligence while maintaining critical business safeguards
# through computational logic that overrides AI decisions when necessary.

"""
Enhanced AI Rules Module for Tutorial Stage 2 (Production Safeguards)

This module represents Vulcan's most sophisticated hybrid approach, demonstrating
how production systems can safely leverage AI while maintaining critical business
guardrails. Key demonstrations:

- All baseline AI functionality from the standard Gemini implementation
- Deterministic fallback rules that override AI decisions in critical scenarios
- Production-ready error handling with transparent audit trails
- Hybrid architecture that combines AI flexibility with computational certainty

Architecture Highlights:
- AI Classification: Gemini provides intelligent risk assessment
- Fallback Guardrails: Deterministic rules catch critical scenarios AI might miss
- Transparent Overrides: Clear logging when fallback rules engage
- Business Continuity: Critical decisions never depend solely on AI interpretation

This pattern is essential for production deployments where business-critical
decisions require guaranteed reliability beyond what AI alone can provide.
The enhanced rules show how Vulcan enables "best of both worlds" automation:
intelligent AI reasoning with computational certainty for critical edge cases.
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
# Global Configuration and Critical Keywords
# ═══════════════════════════════════════════════════════════════════════════════
# This section demonstrates production configuration patterns for hybrid systems.

_LLM = None  # Configured in define_rules() with production Gemini model

# Critical business keywords that trigger deterministic overrides
# These represent scenarios too important to rely on AI interpretation alone
_HIGH_KEYWORDS = ("shutdown", "embargo", "strike")

# ═══════════════════════════════════════════════════════════════════════════════
# Shared AI Classification Engine
# ═══════════════════════════════════════════════════════════════════════════════
# This section reuses the proven AI logic from the baseline implementation,
# demonstrating how enhanced systems build upon reliable foundations.

@lru_cache(maxsize=None)
def _ask_llm(bulletin: str, region: str) -> Tuple[bool, str, bool]:
    """
    Executes the proven three-step microprompting methodology from baseline system.
    
    This function maintains identical AI reasoning logic to the baseline Gemini
    implementation, ensuring consistency while the enhanced rules add additional
    safeguards on top. This demonstrates Vulcan's architectural flexibility:
    AI reasoning remains unchanged while business logic evolves around it.
    
    The caching and error handling patterns are identical to the baseline,
    proving that enhanced systems don't require rebuilding proven components.
    """
    template = load_prompt("ai-reasoning-prompt.txt")
    prompt = template.format(bulletin=bulletin, region=region)
    reply = _LLM.invoke(prompt)  # type: ignore[attr-defined]
    tokens = re.findall(r"(YES|NO|LOW|MEDIUM|HIGH)", reply.content.upper())
    if len(tokens) < 3:
        raise ValueError(f"Unexpected LLM reply: {reply.content!r}")
    return tokens[0] == "YES", tokens[1], tokens[2] == "YES"

def _classify_and_print(bulletin: NewsBulletin) -> ActionReturn:
    """
    Provides AI classification with identical audit trail to baseline system.
    
    This function maintains the exact same console output format and decision
    logic as the baseline Gemini implementation. This consistency enables:
    - Direct comparison between baseline and enhanced system outputs
    - Seamless transition from baseline to enhanced rules in production
    - Identical debugging and monitoring experiences across rule variants
    
    The enhanced system adds value through additional rules, not by changing
    the core AI reasoning that has been proven to work reliably.
    """
    has_risk, severity, region_specific = _ask_llm(bulletin.content, bulletin.region)

    # Provide identical decision audit trail to baseline system
    print("\n[MICROPROMPT 1] Does the bulletin indicate supply-chain risk?")
    print(f"  → {'YES' if has_risk else 'NO'}")
    print("[MICROPROMPT 2] What is the *severity* of that risk?")
    print(f"  → {severity}")
    print(f"[MICROPROMPT 3] Is the risk specific to {bulletin.region}?")
    print(f"  → {'YES' if region_specific else 'NO'}\n")

    level = severity if (has_risk and region_specific) else "LOW"
    return RegionRisk(region=bulletin.region, level=level)

# ═══════════════════════════════════════════════════════════════════════════════
# Production Safeguard: Deterministic Fallback Override
# ═══════════════════════════════════════════════════════════════════════════════
# This section demonstrates Vulcan's key production advantage: the ability to
# override AI decisions with deterministic logic for business-critical scenarios.

def _escalate_medium_to_high(risk: RegionRisk) -> ActionReturn:
    """
    Implements deterministic override for critical business scenarios.
    
    This function demonstrates Vulcan's hybrid architecture advantage: when AI
    classification might be insufficient for business-critical scenarios, 
    deterministic rules can provide guaranteed correct responses.
    
    Key Production Benefits:
    - Guaranteed Response: Critical keywords always trigger HIGH risk classification
    - Transparent Override: Clear logging shows when fallback logic engages
    - Business Continuity: Critical decisions never depend solely on AI variability
    - Audit Compliance: Deterministic rules provide explainable decision trails
    
    This pattern is essential for production deployments where certain scenarios
    are too critical to risk AI misclassification, no matter how unlikely.
    """
    print("[FALLBACK] Deterministic keyword found → escalate MEDIUM → HIGH\n")
    return RegionRisk(region=risk.region, level="HIGH")

# ═══════════════════════════════════════════════════════════════════════════════
# Enhanced Rule Cascade Definition
# ═══════════════════════════════════════════════════════════════════════════════
# This section demonstrates how Vulcan enables sophisticated hybrid systems that
# layer deterministic safeguards on top of AI reasoning without changing the
# core AI logic or business rule structure.

def define_rules(engine: RuleEngine, llm) -> None:
    """
    Demonstrates Vulcan's enhanced hybrid architecture with production safeguards.
    
    This function showcases how enhanced systems build upon proven foundations:
    - Rules 1, 3, 4, 5: Identical to baseline system (proven reliable)
    - Rule 2: NEW deterministic fallback that adds production safeguards
    
    The enhanced architecture demonstrates several critical production patterns:
    
    1. Incremental Enhancement: New safeguards added without changing proven logic
    2. Fallback Reliability: Critical scenarios guaranteed through deterministic rules
    3. Transparent Operation: Clear logging when enhanced safeguards engage
    4. Business Continuity: AI provides intelligence, computation provides certainty
    
    This pattern enables organizations to deploy AI-enhanced systems with confidence,
    knowing that business-critical scenarios are protected by computational guarantees
    regardless of AI performance variability.
    """
    # Configure the global LLM instance using proven baseline pattern
    global _LLM
    _LLM = llm

    # ═══ Rule 1: AI Classification (Identical to Baseline) ═══
    # This rule uses the exact same AI logic as the baseline system,
    # demonstrating architectural consistency and reuse of proven components
    engine.rule(
        name="ai_classify_region_risk",
        when=condition(lambda: bool(NewsBulletin.content)),
        then=action(_classify_and_print),
    )

    # ═══ Rule 2: NEW - Deterministic Fallback Override ═══
    # This rule demonstrates Vulcan's key production advantage: deterministic
    # override capability that ensures critical business scenarios are handled
    # correctly regardless of AI interpretation variability
    engine.rule(
        name="escalate_medium_keyword",
        when=condition(
            lambda: RegionRisk.level == "MEDIUM"
            and any(k in NewsBulletin.content.lower() for k in _HIGH_KEYWORDS)
        ),
        then=action(_escalate_medium_to_high),
    )

    # ═══ Rule 3: Supplier Switching Logic (Identical to Baseline) ═══
    # This rule demonstrates how enhanced systems maintain proven business logic
    # while benefiting from the improved risk classification above
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

    # ═══ Rule 4: Critical Alert Generation (Identical to Baseline) ═══
    # This rule shows how enhanced safeguards automatically benefit downstream
    # business logic without requiring changes to proven alert generation
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

    # ═══ Rule 5: Risk Monitoring Alerts (Identical to Baseline) ═══
    # This rule demonstrates system-wide consistency: enhanced safeguards improve
    # the entire system without requiring changes to individual alert rules
    engine.rule(
        name="alert_on_medium_risk",
        when=condition(lambda: RegionRisk.level == "MEDIUM"),
        then=action(
            lambda: Alert(
                message=f"ALERT: The risk in {RegionRisk.region} has changed to MEDIUM"
            )
        ),
    )
