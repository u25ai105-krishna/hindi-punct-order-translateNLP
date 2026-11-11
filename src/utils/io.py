import json
from pathlib import Path

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

def load_yaml(path: str) -> dict:
    if YAML_AVAILABLE:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        # Simple fallback parser for basic YAML key-values
        res = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    parts = line.split(":", 1)
                    k = parts[0].strip()
                    v = parts[1].strip().strip('"').strip("'")
                    if v.lower() == "true": v = True
                    elif v.lower() == "false": v = False
                    elif v.replace(".", "", 1).isdigit(): v = float(v) if "." in v else int(v)
                    res[k] = v
        return res

def save_json(data, path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_text(text: str, path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
