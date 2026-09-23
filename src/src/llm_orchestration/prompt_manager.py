"""
Dynamic Contextual Depth (DCD) - Prompt Orchestration Manager
Author: Harshal Gopalani
Description: Dynamically loads and structures LLM prompts based on Routing Telemetry.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger("DCD_PromptManager")

class PromptManager:
    def __init__(self, config_path: str = "constrained_prompts.json"):
        self.config_path = Path(__file__).parent / config_path
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        """Loads the JSON prompt registry into memory safely."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                registry = json.load(file)
                logger.info(f"Loaded Prompt Registry Version: {registry.get('version')}")
                return registry
        except FileNotFoundError:
            logger.critical(f"Prompt registry not found at {self.config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.critical(f"Invalid JSON in prompt registry: {str(e)}")
            raise

    def get_orchestration_config(self, tci_score: int) -> Dict[str, Any]:
        """
        Calculates the correct prompt tier and token budget based on the TCI score.
        """
        base_directive = self.registry.get("base_directive", "")
        
        # O(N) lookup where N is small (3 tiers). 
        # Resolves the exact constraints for the heavy LLM.
        for tier_name, config in self.registry["tiers"].items():
            min_tci, max_tci = config["tci_range"]
            if min_tci <= tci_score <= max_tci:
                final_system_prompt = f"{base_directive}\n\n{config['system_prompt']}"
                
                return {
                    "tier": tier_name,
                    "max_tokens": config["max_tokens"],
                    "system_prompt": final_system_prompt
                }
        
        # Fallback for unexpected TCI scores
        logger.warning(f"TCI {tci_score} out of bounds. Defaulting to medium_complexity.")
        default_config = self.registry["tiers"]["medium_complexity"]
        return {
            "tier": "medium_complexity_fallback",
            "max_tokens": default_config["max_tokens"],
            "system_prompt": f"{base_directive}\n\n{default_config['system_prompt']}"
        }

# ---------------------------------------------------------
# Local Execution Test
# ---------------------------------------------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    manager = PromptManager()
    
    print("\n--- Simulating TCI = 2 (Simple Fact) ---")
    print(json.dumps(manager.get_orchestration_config(2), indent=2))
    
    print("\n--- Simulating TCI = 9 (Deep Architectural Query) ---")
    print(json.dumps(manager.get_orchestration_config(9), indent=2))
