import json
from pathlib import Path

def load_config(config_path='src/config.json'):
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)
