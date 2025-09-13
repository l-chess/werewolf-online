from collections import Counter

# Group repeated roles for display and return
def group_roles(roles):
    grouped = []
    for role, count in Counter(roles).most_common():
        grouped.extend([role] * count)
    return grouped