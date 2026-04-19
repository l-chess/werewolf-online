def build_roleset(roles, all_roles, included_roles, num_players, num_stackables):
    import random

    selected_roles = []
    used_roles = set()
    stackables = []

    # Include user-specified roles
    for role in included_roles:
        meta = roles.get(role, {})

        if meta.get("stackable", False):
            if role not in stackables and len(stackables) < max_stackables:
                stackables.append(role)
            continue
        if not meta.get("repeatable", False) and role in used_roles:
            continue

        required = meta.get("requires", [])
        required_to_add = [r for r in required if r not in selected_roles]

        if len(selected_roles) + 1 + len(required_to_add) > num_players:
            continue  # Not enough space, skip this role

        for req in required_to_add:
            req_meta = roles.get(req, {})
            if req_meta and (
                req_meta.get("stackable", False)
                or (not req_meta.get("repeatable", False) and req in used_roles)
            ):
                break  # Dependency conflict
            selected_roles.append(req)
            used_roles.add(req)

        selected_roles.append(role)
        used_roles.add(role)

    # Create set for main/non-stackable roles
    while len(selected_roles) < num_players:
        role = random.choice(all_roles)
        meta = roles[role]

        if meta.get("stackable", False):
            continue

        if not meta.get("repeatable", False) and role in used_roles:
            continue

        required = meta.get("requires", [])
        required_to_add = [r for r in required if r not in selected_roles]

        if len(selected_roles) + 1 + len(required_to_add) > num_players:
            continue

        for req in required_to_add:
            req_meta = roles.get(req)
            if req_meta and (
                req_meta.get("stackable", False)
                or (not req_meta.get("repeatable", False) and req in used_roles)
            ):
                break
            selected_roles.append(req)
            used_roles.add(req)

        selected_roles.append(role)
        used_roles.add(role)

    # Choose stackable roles
    # Choose stackable roles and handle their dependencies
    while (
        len(stackables) < num_stackables
        and len(selected_roles) + len(stackables) < num_players
    ):
        role = random.choice(all_roles)
        meta = roles[role]

        if not meta.get("stackable", False):
            continue
        if role in stackables:
            continue

        # Handle required roles for stackable
        required = meta.get("requires", [])
        required_to_add = [
            r for r in required if r not in selected_roles and r not in stackables
        ]

        # Check if adding this stackable and its required roles would exceed player limit
        if (
            len(selected_roles) + len(stackables) + 1 + len(required_to_add)
            > num_players
        ):
            continue

        # Check if required roles violate constraints
        conflict = False
        for req in required_to_add:
            req_meta = roles.get(req)
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

    return selected_roles, stackables
