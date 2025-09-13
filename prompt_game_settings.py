def prompt_game_settings():
    try:
        num_players = int(input("Wie viele Spieler spielen mit? "))
        target_sum = int(input("Bevorzugter Punktewert: "))
        return num_players, target_sum
    except ValueError:
        print("Bitte gib gültige Zahlen ein.")
        return None, None
