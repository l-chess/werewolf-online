import json
from user_prompts import prompt_user_for_roles, prompt_game_settings
from role_utils import build_name_map, resolve_roles_by_name


def load_roles(path="roles.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            roles = json.load(f)
    except FileNotFoundError:
        print(f"Die Datei {path} wurde nicht gefunden.")
        return None, None, None, None

    included_roles = prompt_user_for_roles(
        roles, build_name_map(roles), resolve_roles_by_name
    )

    num_players, target_sum = prompt_game_settings()
    if num_players is None or target_sum is None:
        return None, None, None, None

    all_roles = list(roles.keys())

    return roles, included_roles, num_players, target_sum, all_roles
