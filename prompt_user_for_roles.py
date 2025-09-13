def prompt_user_for_roles(roles_dict, name_map, resolve_roles_by_name):
    included_roles = []

    use_specific = input("Möchtest du bestimmte Rollen benutzen? (y/n): ").strip().lower()
    if use_specific == 'y':
        while True:
            raw_input = input("Welche Rollen möchtest du benutzen?\n").strip()
            user_inputs = [r.strip() for r in raw_input.split(",")]

            resolved_roles, unknown_names = resolve_roles_by_name(user_inputs, name_map)

            if unknown_names:
                print("\nEinige Rollen wurden nicht erkannt:")
                for name in unknown_names:
                    print(f"- '{name}'")
                retry = input("Möchtest du es nochmal versuchen? (y/n): ").strip().lower()
                if retry == 'y':
                    continue
                else:
                    print("Set wird ohne vorbestimmte Rollen erstellt. \n")
                    break
            else:
                print(f"{len(resolved_roles)} Rollen werden eingebunden.\n")
                included_roles = resolved_roles
                break
    return included_roles
