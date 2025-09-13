def load_roles(path):
    import json
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Die Datei {path} wurde nicht gefunden.")
        return None
