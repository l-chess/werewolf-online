def assign_roles(selected_roles=None, stackables=None):
    import random

    if selected_roles is None:
        roles_input = input("Welche Rollen gibt es?\n")
        selected_roles = [r.strip() for r in roles_input.split(",")]

    if stackables is None:
        stackables = []

    player_input = input("Wer spielt mit?\n")
    players = [p.strip() for p in player_input.split(",")]

    if len(players) != len(selected_roles):
        print("Anzahl der Spieler stimmt nicht mit der Anzahl der Hauptrollen überein.")
        return

    random.shuffle(players)

    print("\nRollenzuweisung:")
    for role, player in zip(selected_roles, players):
        print(f"{role} → {player}")

    # Assign stackables randomly to players
    if stackables:
        print("\nZusätzliche Rollen:")
        for extra_role in stackables:
            assigned_player = random.choice(players)
            print(f"{extra_role} → {assigned_player}")
    print("\n")
