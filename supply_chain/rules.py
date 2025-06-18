# ═══════════════════════════════════════════════════════════════════════════════
# Stage 0: Pure Deterministic Rules Demo
# ═══════════════════════════════════════════════════════════════════════════════
# This module demonstrates Vulcan's foundation: pure computational logic.
# These rules use no AI components, showing how traditional rule engines work
# before adding predictive capabilities. This creates the baseline for
# understanding Vulcan's hybrid approach in later tutorial stages.

from vulcan_core import RuleEngine, action, condition
from .schema import NewsBulletin, RegionRisk, Supplier, ActiveSupplier, Alert


def define_rules(engine: RuleEngine) -> None:
    """
    Demonstrates Vulcan's deterministic rule cascade approach.
    
    This function showcases core Vulcan concepts through a realistic supply chain
    scenario. The five-rule cascade demonstrates:
    
    - How Facts trigger Conditions automatically when they change
    - How Actions modify the knowledge base, triggering further rules  
    - How complex business logic emerges from simple, testable rules
    - Why this approach provides explainable, auditable decisions
    
    Tutorial Learning Points:
    - Rule dependencies create intelligent cascading behavior
    - Each rule is focused and testable in isolation
    - The engine determines rule firing order, not the developer
    - Deterministic logic provides reliable, consistent results
    """

    # ═══════════════════════════════════════════════════════════════════════════════
    # Risk Classification Rules
    # ═══════════════════════════════════════════════════════════════════════════════
    # These rules demonstrate how Vulcan automatically processes trigger events
    # and classifies risk levels based on content analysis.

    # Rule 1: HIGH Risk Detection - Tariff/Trade Policy Events
    # This rule shows how keyword detection can trigger immediate escalation
    # Tariffs represent severe supply chain disruption requiring supplier switching
    engine.rule(
        name="detect_high_regional_risk",
        when=condition(lambda: "tariff" in NewsBulletin.content),
        then=action(
            lambda: RegionRisk(region=NewsBulletin.region, level="HIGH")
        ),
    )

    # Rule 2: MEDIUM Risk Detection - Operational Disruptions  
    # This rule demonstrates compound conditions and exclusion logic
    # Operational issues are serious but don't require immediate supplier changes
    engine.rule(
        name="detect_medium_regional_risk",
        when=condition(
            lambda: ("Transportation delays" in NewsBulletin.content or "shortage" in NewsBulletin.content)
            and "tariff" not in NewsBulletin.content
        ),
        then=action(
            lambda: RegionRisk(region=NewsBulletin.region, level="MEDIUM")
        ),
    )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Business Logic Rules
    # ═══════════════════════════════════════════════════════════════════════════════
    # These rules demonstrate how Vulcan handles complex multi-condition logic
    # and cascading business decisions automatically.

    # Rule 3: Supplier Switching Logic - Critical Risk Response
    # This rule showcases Vulcan's strength in complex conditional logic
    # It demonstrates how multiple conditions combine to trigger business actions
    active_supplier_high_risk = condition(
        lambda: RegionRisk.level == "HIGH"
        and ActiveSupplier.supplier_region == RegionRisk.region
    )

    backup_supplier_available = condition(
        lambda: Supplier.region != ActiveSupplier.supplier_region
        and RegionRisk.region == Supplier.region
        and RegionRisk.level == "LOW"
    )

    supplier_switch_needed = active_supplier_high_risk & backup_supplier_available

    engine.rule(
        name="switch_supplier_on_high_risk",
        when=supplier_switch_needed,
        then=action(
            lambda: ActiveSupplier(supplier_name=Supplier.name, supplier_region=Supplier.region)
        ),
    )

    # ═══════════════════════════════════════════════════════════════════════════════
    # Alert Generation Rules  
    # ═══════════════════════════════════════════════════════════════════════════════
    # These rules demonstrate how Vulcan can generate different types of
    # notifications based on system state changes.

    # Rule 4: Critical Alert - Supplier Change Notification
    # This rule fires automatically when Rule 3 changes the active supplier
    # It demonstrates how Vulcan's forward-chaining creates intelligent workflows
    engine.rule(
        name="alert_on_supplier_switch",
        when=condition(
            lambda: ActiveSupplier.supplier_region != "Eastern Corridor"
        ),
        then=action(
            lambda: Alert(
                message=(
                    f"CRITICAL ALERT: The new primary supplier is "
                    f"{ActiveSupplier.supplier_name}, ({ActiveSupplier.supplier_region})"
                )
            )
        ),
    )

    # Rule 5: Informational Alert - Medium Risk Monitoring
    # This rule demonstrates different alert severities for different risk levels
    # It shows how the same triggering event can produce multiple types of responses
    engine.rule(
        name="alert_on_medium_risk",
        when=condition(lambda: RegionRisk.level == "MEDIUM"),
        then=action(
            lambda: Alert(
                message=f"ALERT: The risk in {RegionRisk.region} has changed to MEDIUM"
            )
        ),
    )
