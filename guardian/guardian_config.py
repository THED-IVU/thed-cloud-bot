# guardian/guardian_config.py

import json
from pathlib import Path

CONFIG_PATH = Path("guardian/guardian_settings.json")

DEFAULTS = {
    "mode_auto": False,
    "niveau_analyse": "normal",
    "impact_minimal": 50
}

def charger_config():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULTS
    else:
        return DEFAULTS

def sauvegarder_config(config):
    CONFIG_PATH.parent.mkdir(exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
