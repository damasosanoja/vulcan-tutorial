# ═══════════════════════════════════════════════════════════════════════════════
# Supply Chain Domain Model Schema  
# ═══════════════════════════════════════════════════════════════════════════════
# This module defines the fact schema that represents our supply chain domain.
# These fact classes demonstrate Vulcan's knowledge representation approach:
# business concepts are modeled as immutable facts that capture both static
# information and dynamic state changes throughout the decision process.

"""
Supply Chain Tutorial Domain Schema

This module defines the complete fact schema for the Vulcan supply chain tutorial,
demonstrating how to model business domains using Vulcan's fact-based knowledge
representation. Each fact class serves specific tutorial purposes:

Key Learning Demonstrations:
- How to model business entities as immutable facts
- The relationship between input facts, decision facts, and output facts
- Why type constraints (Literal types) improve rule reliability
- How fact schemas enable explainable business logic

Business Process Modeling:
- External events trigger internal decision processes
- Risk assessment drives operational changes  
- Decision audit trails emerge naturally from fact relationships
- System state is completely represented by fact collections

The schema supports all three tutorial stages (deterministic, mock AI, real AI)
without modification, demonstrating Vulcan's architectural flexibility: the same
domain model works regardless of the underlying decision logic complexity.
"""

from typing import Literal
from vulcan_core import Fact

# ═══════════════════════════════════════════════════════════════════════════════
# Infrastructure and Configuration Facts
# ═══════════════════════════════════════════════════════════════════════════════
# These facts represent the static elements of our supply chain that provide
# the foundation for decision making: available suppliers and their capabilities.

class Supplier(Fact):
    """
    Represents a supplier in our supply chain network.
    
    This fact demonstrates Vulcan's approach to modeling business entities:
    simple, focused data structures that capture essential information without
    unnecessary complexity. The regional attribute enables geographic risk
    assessment, while the name provides human-readable identification.
    
    Tutorial Learning Points:
    - Facts represent business entities as immutable data structures
    - Simple schemas enable clear rule logic without complex object hierarchies
    - Geographic attributes enable sophisticated risk-based decision making
    - Fact attributes can be referenced directly in rule conditions
    
    Business Context:
    - Suppliers provide our raw materials and components
    - Geographic distribution enables risk mitigation strategies
    - Multiple suppliers in different regions provide operational resilience
    - Supplier switching decisions depend on both capability and location
    """
    name: str          # Human-readable supplier identification
    region: str        # Geographic location for risk assessment

# ═══════════════════════════════════════════════════════════════════════════════
# External Event Facts
# ═══════════════════════════════════════════════════════════════════════════════
# These facts represent information flowing into our system from external sources,
# triggering the decision processes that our rules will orchestrate.

class NewsBulletin(Fact):
    """
    Represents external information that may affect supply chain decisions.
    
    This fact demonstrates how Vulcan integrates external data sources into
    decision processes. The content field provides unstructured information
    for AI analysis, while the region field enables geographic correlation
    with our supplier network and risk assessments.
    
    Tutorial Learning Points:
    - External events are modeled as facts, not function parameters
    - Unstructured content (news text) can be processed by AI-enhanced rules
    - Geographic correlation enables intelligent decision routing
    - Facts provide clean separation between data input and rule logic
    
    Business Context:
    - News events may indicate emerging supply chain risks
    - Regional correlation helps identify which suppliers are affected
    - Content analysis (via AI) determines risk severity and type
    - Single bulletins can trigger complex multi-step decision cascades
    """
    content: str       # Unstructured text for AI analysis and keyword detection
    region: str        # Geographic scope for correlation with supplier locations

# ═══════════════════════════════════════════════════════════════════════════════
# Decision State Facts
# ═══════════════════════════════════════════════════════════════════════════════
# These facts represent the intermediate and final results of our decision
# processes, capturing both risk assessments and operational decisions.

class RegionRisk(Fact):
    """
    Represents the assessed risk level for a specific geographic region.
    
    This fact demonstrates Vulcan's approach to intermediate decision state:
    AI classification results are captured as facts that can then drive
    deterministic business logic. The Literal type constraint ensures
    reliable downstream processing by preventing invalid risk levels.
    
    Tutorial Learning Points:
    - AI decisions are captured as structured facts, not raw text responses
    - Type constraints (Literal) prevent invalid state in business logic
    - Intermediate facts enable multi-step decision processes
    - Risk levels drive different business responses (alerts vs supplier switches)
    
    Business Context:
    - Risk levels are determined by AI analysis of news content
    - HIGH risk triggers immediate supplier switching logic
    - MEDIUM risk generates monitoring alerts without operational changes
    - LOW risk represents normal operating conditions
    - Regional scope enables targeted response to localized threats
    """
    region: str                                    # Geographic area being assessed
    level: Literal["HIGH", "MEDIUM", "LOW"]       # Constrained risk classification

class ActiveSupplier(Fact):
    """
    Represents the currently operational supplier for our supply chain.
    
    This fact demonstrates Vulcan's approach to operational state tracking:
    current system configuration is explicitly modeled as facts that can
    be monitored and modified by rules. Changes to this fact trigger
    cascade effects through alert generation and compliance checking.
    
    Tutorial Learning Points:
    - Operational state is explicitly tracked through facts
    - State changes trigger automatic rule cascades
    - Current configuration drives conditional business logic
    - Fact updates provide natural audit trails for decisions
    
    Business Context:
    - Tracks which supplier is currently handling our operations
    - Changes trigger critical alerts for stakeholder notification
    - Regional information enables geographic risk correlation
    - Supplier switching decisions update this operational state
    - Historical changes provide audit trail for business decisions
    """
    supplier_name: str     # Identity of the currently active supplier
    supplier_region: str   # Geographic location of current operations

# ═══════════════════════════════════════════════════════════════════════════════
# Output and Communication Facts
# ═══════════════════════════════════════════════════════════════════════════════
# These facts represent the outputs of our decision system: notifications,
# alerts, and communications generated for human stakeholders.

class Alert(Fact):
    """
    Represents a notification or alert generated by the decision system.
    
    This fact demonstrates Vulcan's approach to system outputs: instead of
    direct I/O operations (print statements, emails, etc.), rule systems
    generate facts that represent intended communications. This pattern
    enables testing, audit trails, and flexible output routing.
    
    Tutorial Learning Points:
    - System outputs are modeled as facts, not side effects
    - Alert generation can be conditional based on system state
    - Messages provide human-readable explanations of system decisions
    - Fact-based outputs enable testing and audit trail creation
    
    Business Context:
    - Critical alerts notify stakeholders of supplier changes
    - Informational alerts provide risk level monitoring
    - Message content explains the business reasoning behind decisions
    - Alert generation demonstrates how rules create communication workflows
    - Different alert types enable graduated stakeholder responses
    """
    message: str       # Human-readable description of the alert or notification
