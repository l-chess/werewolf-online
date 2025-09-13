from assign_roles import assign_roles
from find_balanced_roles import find_balanced_roles

generate_set = input("Do you want to generate a roleset? (y/n) ")

if generate_set.strip().lower() == "y":
    find_balanced_roles()
else:
    role_assignment = input("Do you want to assign roles? (y/n) ")
    if role_assignment.strip().lower() == "y":
        assign_roles()