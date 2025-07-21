def find_balanced_roles(
    roles_file='roles.json', 
    max_attempts=10000, 
    max_stackables=3
):
    from assign_roles import assign_roles

    import json
    import random

    # Load roles from roles.json
    try:
        with open(roles_file, 'r', encoding='utf-8') as file:
            roles_dict = json.load(file)
    except FileNotFoundError:
        print(f"Die Datei {roles_file} wurde nicht gefunden.")
        return None, None, None

    # Take user input for number of players and target balance sum
    try:
        num_players = int(input("Wie viele Spieler spielen mit? "))
        target_sum = int(input("Bevorzugter Punktewert: "))
    except ValueError:
        print("Bitte gib gültige Zahlen ein.")
        return None, None, None

    all_roles = list(roles_dict.keys())

    for _ in range(max_attempts): # Loop for max_attempts to create a valid role combination
        selected_roles = []
        used_roles = set()

        num_stackables = random.randint(0, min(max_stackables, num_players))
        stackables = []

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
        while len(stackables) < num_stackables:
            role = random.choice(all_roles)
            meta = roles_dict[role]

            if not meta.get("stackable", False):
                continue
            if role in stackables:
                continue
            stackables.append(role)

        total_roles = selected_roles + stackables

        if not all(r in roles_dict for r in total_roles):
            continue

        total_points = sum(roles_dict[r]["points"] for r in total_roles)

        if total_points == target_sum:
            print("Zugewiesene Hauptrollen:")
            for r in selected_roles:
                print(f"- {r} ({roles_dict[r]['points']} Punkte)")

            if stackables:
                print("\nZusätzliche Rollen (werden zusätzlich vergeben):")
                for r in stackables:
                    print(f"- {r} ({roles_dict[r]['points']} Punkte)")

            print(f"\nGesamtpunkte (inklusive Zusatzrollen): {total_points}")

            # Prompt user to assign roleset to players
            assign_now = input("\nMöchtest du diese Rollen jetzt zuweisen? (y/n): ").strip().lower()
            if assign_now == 'y':
                assign_roles(selected_roles, stackables)

            return selected_roles, stackables, total_points

    print("Keine passende Kombination gefunden.")
    return None, None, None