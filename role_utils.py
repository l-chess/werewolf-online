from collections import Counter


# maps technical names to actual roles
def build_name_map(roles_dict):
    name_map = {}
    for role, data in roles_dict.items():
        name_map[role.lower()] = role
        for alias in data.get("technical", []):
            name_map[alias.lower()] = role
    return name_map


# resolves user input for roles
def resolve_roles_by_name(input_names, name_map):
    resolved = []
    unknown = []
    for name in input_names:
        role = name_map.get(name.lower())
        if role:
            resolved.append(role)
        else:
            unknown.append(name)
    return resolved, unknown


# Group repeated roles for display and return
def group_roles(roles):
    grouped = []
    for role, count in Counter(roles).most_common():
        grouped.extend([role] * count)
    return grouped
