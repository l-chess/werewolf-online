def build_name_map(roles_dict):
    """
    Builds a mapping from lowercase names and technical aliases
    to canonical role names.
    """
    name_map = {}
    for role, data in roles_dict.items():
        name_map[role.lower()] = role
        for alias in data.get("technical", []):
            name_map[alias.lower()] = role
    return name_map


def resolve_roles_by_name(input_names, name_map):
    """
    Resolves a list of user input names (lowercased) to valid roles.
    Returns a tuple: (resolved_roles, unknown_names)
    """
    resolved = []
    unknown = []
    for name in input_names:
        role = name_map.get(name.lower())
        if role:
            resolved.append(role)
        else:
            unknown.append(name)
    return resolved, unknown
