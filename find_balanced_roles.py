def find_balanced_roles(
    roles_file='roles.json', 
    max_attempts=10000, 
    max_stackables=3
):
    from assign_roles import assign_roles
    from load_roles import load_roles
    from prompt_user_for_roles import prompt_user_for_roles
    from prompt_game_settings import prompt_game_settings

    import json
    import random

    # Load roles from roles.json
    roles_dict = load_roles(roles_file)
    if roles_dict is None:
        return None, None, None

    from role_utils import build_name_map, resolve_roles_by_name
    name_map = build_name_map(roles_dict)
    included_roles = prompt_user_for_roles(roles_dict, name_map, resolve_roles_by_name)


    # Take user input for number of players and target balance sum
    num_players, target_sum = prompt_game_settings()
    if num_players is None or target_sum is None:
        return None, None, None


    all_roles = list(roles_dict.keys())

    for _ in range(max_attempts): # Loop for max_attempts to create a valid role combination
        selected_roles = []
        used_roles = set()

        num_stackables = random.randint(0, min(max_stackables, num_players))
        stackables = []

        # Include user-specified roles
        for role in included_roles:
            meta = roles_dict.get(role, {})

            if meta.get("stackable", False):
                if role not in stackables and len(stackables) < max_stackables:
                    stackables.append(role)
                continue
            if not meta.get("repeatable", False) and role in used_roles:
                continue

            required = meta.get("requires", [])
            required_to_add = [r for r in required if r not in selected_roles]

            if len(selected_roles) + 1 + len(required_to_add) > num_players:
                continue # Not enough space, skip this role

            for req in required_to_add:
                req_meta = roles_dict.get(req, {})
                if req_meta and (req_meta.get("stackable", False) or (not req_meta.get("repeatable", False) and req in used_roles)):
                    break # Dependency conflict
                selected_roles.append(req)
                used_roles.add(req)

            selected_roles.append(role)
            used_roles.add(role)

        # Create set for main/non-stackable roles
        while len(selected_roles) < num_players:
            role = random.choice(all_roles)
            meta = roles_dict[role]

            if meta.get("stackable", False):
                continue

            if not meta.get("repeatable", False) and role in used_roles:
                continue

            required = meta.get("requires", [])
            required_to_add = [r for r in required if r not in selected_roles]

            if len(selected_roles) + 1 + len(required_to_add) > num_players:
                continue

            for req in required_to_add:
                req_meta = roles_dict.get(req)
                if req_meta and (req_meta.get("stackable", False) or (not req_meta.get("repeatable", False) and req in used_roles)):
                    break
                selected_roles.append(req)
                used_roles.add(req)

            selected_roles.append(role)
            used_roles.add(role)

        # Choose stackable roles
                # Choose stackable roles and handle their dependencies
        while len(stackables) < num_stackables and len(selected_roles) + len(stackables) < num_players:
            role = random.choice(all_roles)
            meta = roles_dict[role]

            if not meta.get("stackable", False):
                continue
            if role in stackables:
                continue

            # Handle required roles for stackable
            required = meta.get("requires", [])
            required_to_add = [r for r in required if r not in selected_roles and r not in stackables]

            # Check if adding this stackable and its required roles would exceed player limit
            if len(selected_roles) + len(stackables) + 1 + len(required_to_add) > num_players:
                continue

            # Check if required roles violate constraints
            conflict = False
            for req in required_to_add:
                req_meta = roles_dict.get(req)
                if not req_meta:
                    conflict = True
                    break
                if req_meta.get("stackable", False):
                    conflict = True
                    break
                if not req_meta.get("repeatable", False) and req in selected_roles:
                    conflict = True
                    break
            if conflict:
                continue

            # Add required roles
            for req in required_to_add:
                selected_roles.append(req)
                used_roles.add(req)

            # Add the stackable
            stackables.append(role)

        total_roles = selected_roles + stackables

        if not all(r in roles_dict for r in total_roles):
            continue

        total_points = sum(roles_dict[r]["points"] for r in total_roles)

        if total_points == target_sum:
            from group_roles import group_roles
            
            # group repeated roles
            selected_roles = group_roles(selected_roles)
            stackables = group_roles(stackables)

            print("Zugewiesene Hauptrollen:")
            for r in selected_roles:
                print(f"- {r} ({roles_dict[r]['points']} Punkte)")

            if stackables:
                print("\nZusätzliche Rollen (werden zusätzlich vergeben):")
                for r in stackables:
                    print(f"- {r} ({roles_dict[r]['points']} Punkte)")

            # Prompt user to assign roleset to players
            assign_now = input("\nMöchtest du diese Rollen jetzt zuweisen? (y/n): ").strip().lower()
            if assign_now == 'y':
                assign_roles(selected_roles, stackables)

            return selected_roles, stackables, total_points

    print("Keine passende Kombination gefunden.")
    return None, None, None