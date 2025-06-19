# ═══════════════════════════════════════════════════════════════════════════════
# Initial State Configuration for Supply Chain Tutorial
# ═══════════════════════════════════════════════════════════════════════════════
# This module defines the baseline facts that represent our supply chain's
# starting state before any events occur. These facts establish the "known world"
# that Vulcan will reason about, demonstrating how working memory is initialized
# with business-relevant information before rule evaluation begins.

"""
Supply Chain Initial State Configuration

This module demonstrates Vulcan's fact-based knowledge representation by defining
the baseline state of our supply chain system. These initial facts serve multiple
tutorial purposes:

Architectural Demonstrations:
- How to pre-populate Vulcan's working memory with business context
- The relationship between different fact types in a domain model
- How initial state establishes the foundation for rule-based reasoning

Business Context Setup:
- Two-supplier scenario (primary + backup) for risk mitigation demonstrations
- Regional risk baselines that can be modified by external events  
- Active supplier tracking that enables dynamic switching logic

Tutorial Integration:
- Used by all tutorial stages: demo.py scenarios 1-4
- Loaded by both mock simulation (runners/mock_simulation.py) and real AI (runners/ai_integration.py)
- Provides consistent starting conditions across all tutorial demonstrations

The facts defined here represent "what we know before today's news affects our
decisions" - they establish the stable business context that incoming events
will test and potentially modify through our rule cascades.
"""

from .schema import Supplier, RegionRisk, ActiveSupplier

# ═══════════════════════════════════════════════════════════════════════════════
# Supplier Infrastructure Facts
# ═══════════════════════════════════════════════════════════════════════════════
# These facts establish our supply chain's operational infrastructure.
# The two-supplier setup demonstrates risk mitigation through geographic diversity
# and enables the tutorial's supplier switching demonstrations.

# Primary supplier located in our main operational region
# This supplier handles our baseline operations under normal conditions
# Used in demo scenarios 1-4 to demonstrate different risk response patterns
INITIAL_SUPPLIER = Supplier(name="CyberSystems Inc.", region="Eastern Corridor")

# Backup supplier in an alternative region for risk mitigation
# This supplier provides operational continuity when primary region faces disruption
# Becomes active when demo scenarios trigger HIGH risk conditions (scenario 1, 4)
BACKUP_SUPPLIER = Supplier(name="TechFlow Solutions", region="Western Corridor")

# ═══════════════════════════════════════════════════════════════════════════════
# Operational State Tracking
# ═══════════════════════════════════════════════════════════════════════════════
# This fact tracks which supplier is currently handling our operations.
# It serves as the key decision state that our rules will monitor and potentially modify
# throughout the tutorial demonstration scenarios.

# Current active supplier configuration
# This fact will be updated by our rules when risk conditions require supplier switching
# Initially set to primary supplier under normal operating conditions
# Watch this fact change during demo scenarios 1 and 4 (HIGH risk events)
INITIAL_ACTIVE_SUPPLIER = ActiveSupplier(
    supplier_name="CyberSystems Inc.", 
    supplier_region="Eastern Corridor"
)

# ═══════════════════════════════════════════════════════════════════════════════
# Regional Risk Assessment Baseline
# ═══════════════════════════════════════════════════════════════════════════════
# These facts establish baseline risk levels for each operational region.
# They provide the starting point for AI-enhanced risk classification that
# incoming events will test and potentially modify across all tutorial stages.

# Eastern Corridor baseline risk assessment
# This region hosts our primary supplier and starts at LOW risk
# External events may cause AI/rules to escalate this risk level:
# - Demo scenario 1: Escalates to HIGH (tariff crisis)
# - Demo scenario 2: Remains LOW (normal operations)  
# - Demo scenario 3: Escalates to MEDIUM (shipping delays)
# - Demo scenario 4: Tests enhanced fallback rules
INITIAL_REGION_RISK_EASTERN = RegionRisk(region="Eastern Corridor", level="LOW")

# Western Corridor baseline risk assessment  
# This region hosts our backup supplier and also starts at LOW risk
# The LOW risk level makes it an attractive fallback option when primary region risk escalates
# This region typically remains stable throughout tutorial scenarios
INITIAL_REGION_RISK_WESTERN = RegionRisk(region="Western Corridor", level="LOW")
