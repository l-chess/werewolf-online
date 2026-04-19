def find_balanced_roles(max_attempts=10000, max_stackables=3):
    from assign_roles import assign_roles
    from load_roles import load_roles
    from build_roleset import build_roleset

    import random

    roles, included_roles, num_players, target_sum, all_roles = load_roles()

    for _ in range(
        max_attempts
    ):  # Loop for max_attempts to create a valid role combination
        num_stackables = random.randint(0, min(max_stackables, num_players))

        selected_roles, stackables = build_roleset(
            roles, all_roles, included_roles, num_players, num_stackables
        )

        total_roles = selected_roles + stackables

        if not all(r in roles for r in total_roles):
            continue

        total_points = sum(roles[r]["points"] for r in total_roles)

        if total_points == target_sum:
            from role_utils import group_roles

            # group repeated roles
            selected_roles = group_roles(selected_roles)
            stackables = group_roles(stackables)

            print("Zugewiesene Hauptrollen:")
            for r in selected_roles:
                print(f"- {r} ({roles[r]['points']} Punkte)")

            if stackables:
                print("\nZusätzliche Rollen (werden zusätzlich vergeben):")
                for r in stackables:
                    print(f"- {r} ({roles[r]['points']} Punkte)")

            # Prompt user to assign roleset to players
            assign_now = (
                input("\nMöchtest du diese Rollen jetzt zuweisen? (y/n): ")
                .strip()
                .lower()
            )
            if assign_now.lower() == "y":
                assign_roles(selected_roles, stackables)

            return selected_roles, stackables, total_points

    print("Keine passende Kombination gefunden.")
    return None, None, None
