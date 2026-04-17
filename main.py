from assign_roles import assign_roles
from find_balanced_roles import find_balanced_roles

if input("Möchtest du ein Rollenset erstellen? (y/n): ").strip().lower() == "y":
    find_balanced_roles()
else:
    if input("Möchtest du Rollen zuweisen? (y/n): ").strip().lower() == "y":
        assign_roles()
