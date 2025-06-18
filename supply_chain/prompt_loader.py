# ═══════════════════════════════════════════════════════════════════════════════
# Prompt Template Management Utility
# ═══════════════════════════════════════════════════════════════════════════════
# This module demonstrates Vulcan's best practice for AI integration: clear
# separation of concerns between rule logic and prompt content. By storing
# prompts as external files, we enable non-technical stakeholders to iterate
# on AI instructions without touching code, while maintaining clean architecture.

"""
Prompt Template Loading Utility for Vulcan AI Integration

This module serves a critical architectural purpose in Vulcan applications:
it enables clean separation between business logic (rules) and AI instructions
(prompts). This separation provides several key benefits:

Architectural Benefits:
- Non-technical stakeholders can iterate on AI instructions independently
- Prompt content remains version-controlled but separate from code
- Rule logic stays focused on business decisions, not AI instruction details
- Easy A/B testing of different prompt variations without code changes

Production Benefits:
- Prompts can be externalized to configuration management systems
- Different environments can use different prompt variations
- Clear audit trail for prompt changes separate from code changes
- Simplified localization and multi-language support

The deferred substitution capability allows Vulcan's rule engine to inject
runtime values (like {NewsBulletin.content}) while preserving pre-configured
static values (like {bulletin} and {region}). This hybrid approach maximizes
both flexibility and performance.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

# ═══════════════════════════════════════════════════════════════════════════════
# Project Structure Configuration
# ═══════════════════════════════════════════════════════════════════════════════
# Establish the canonical path to the prompts directory relative to this module.
# This ensures consistent prompt loading regardless of working directory.

_PROMPT_DIR = Path(__file__).parent.parent / "prompts"

# ═══════════════════════════════════════════════════════════════════════════════
# Safe Template Substitution Engine
# ═══════════════════════════════════════════════════════════════════════════════
# This class enables partial template substitution: known values are replaced
# immediately while unknown placeholders are preserved for later Vulcan processing.

class _SafeMap(dict):
    """
    Enables partial template substitution for hybrid prompt management.
    
    This utility class demonstrates a key architectural pattern for AI integration:
    the ability to pre-substitute some template variables while preserving others
    for runtime evaluation by Vulcan's rule engine.
    
    Key Use Cases:
    - Pre-configure static context (region names, business rules)
    - Preserve dynamic placeholders for Vulcan fact substitution
    - Enable prompt templates that work across different deployment environments
    
    Example:
        Template: "Analyze {bulletin} for risks in {region} affecting {Supplier.name}"
        Pre-substitution: {region} → "Eastern Corridor" 
        Vulcan substitution: {bulletin} → actual news content, {Supplier.name} → actual supplier
        
    This two-stage approach optimizes both maintainability and performance:
    static values are resolved once at load time, while dynamic values are
    resolved efficiently during rule evaluation.
    """

    def __missing__(self, key: str) -> str:
        """
        Returns unknown keys as-is instead of raising KeyError.
        
        This method enables the partial substitution pattern: when Python's
        str.format_map() encounters a placeholder we haven't provided a value for,
        it calls this method. Instead of failing, we return the placeholder
        unchanged, preserving it for later Vulcan processing.
        
        Args:
            key: The template placeholder key that wasn't found in our values
            
        Returns:
            The original placeholder wrapped in braces, ready for later substitution
        """
        return "{" + key + "}"

# ═══════════════════════════════════════════════════════════════════════════════
# Main Prompt Loading Interface
# ═══════════════════════════════════════════════════════════════════════════════
# This function provides the primary interface for loading and configuring
# prompt templates in Vulcan applications.

def load_prompt(name: str, **vars: Mapping[str, Any]) -> str:
    """
    Loads and optionally pre-configures prompt templates for AI integration.
    
    This function embodies Vulcan's recommended approach to AI prompt management:
    store prompts as external files for maintainability, then perform partial
    substitution to balance static configuration with dynamic rule evaluation.
    
    The function supports two substitution phases:
    1. Immediate substitution of provided keyword arguments (configuration values)
    2. Deferred substitution of Vulcan fact placeholders (runtime values)
    
    Tutorial Learning Points:
    - Prompt files are stored in /prompts directory for easy maintenance
    - Static configuration values can be pre-substituted for efficiency
    - Vulcan-style placeholders (like {Fact.attribute}) are preserved automatically
    - Error handling ensures missing prompt files are caught early
    
    Production Benefits:
    - Non-technical stakeholders can edit prompts without code changes
    - Environment-specific configuration through keyword arguments
    - Clear separation between static setup and dynamic rule evaluation
    - Version control friendly prompt management
    
    Args:
        name: Filename in the /prompts directory (e.g., "ai-reasoning-prompt.txt")
        **vars: Optional key-value pairs for immediate substitution.
               Placeholders not provided remain untouched for Vulcan processing.
    
    Returns:
        Processed template string ready for Vulcan rule integration.
        Static values are substituted, Vulcan placeholders are preserved.
    
    Raises:
        FileNotFoundError: If the specified prompt file doesn't exist.
        
    Example:
        # Load template with pre-configured region
        template = load_prompt("risk-analysis.txt", region="Eastern Corridor")
        
        # Template before: "Analyze {bulletin} for {region} risks affecting {Supplier.name}"
        # Template after:  "Analyze {bulletin} for Eastern Corridor risks affecting {Supplier.name}"
        
        # Vulcan will later substitute {bulletin} and {Supplier.name} during rule evaluation
    """
    # Construct the full path to the prompt file using our configured directory
    # This approach ensures consistent behavior regardless of working directory
    path = _PROMPT_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {path}")

    # Load the raw template content, removing any trailing whitespace
    # Clean content reduces the chance of formatting issues in AI interactions
    text = path.read_text().strip()
    
    # Perform partial substitution using our safe mapping approach
    # Known values are substituted immediately, unknown placeholders are preserved
    return text.format_map(_SafeMap(vars))
