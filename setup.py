import bcrypt
from getpass import getpass
import os
from colors import cprint

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# shameless plug
cprint("\nurvianoob's Password Manager v1.0\n", "header")

try:
    # if you have these files, then you've already run the setup
    with open(os.path.join(__location__, "password.txt"), "rb") as f:
        f.read()
    with open(os.path.join(__location__, "definitelyNotWhereYourPasswordsAreStored.json"), "rb") as f:
        f.read()

    cprint("Error: you've already setup the password manager\n", "red")

except FileNotFoundError:
    # if files not found, run the setup
    print("Welcome to the initial setup\n")
    print("Please enter a password that's 15 characters or longer\n")

    password = getpass(prompt="Enter your master password: ")
    confirmPassword = getpass(prompt="Confirm your master password: ")
    while password != confirmPassword or len(password) < 15:
        if len(password) < 15:
            cprint("\nPlease enter a password that's 15 characters or longer", "yellow")
        else:
            cprint("\nError: passwords did not match\n", "red")

        password = getpass(prompt="Enter your master password: ")
        confirmPassword = getpass(prompt="Confirm your master password: ")

    x = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    with open(os.path.join(__location__, "password.txt"), "wb") as f:
        f.write(x)

    with open(os.path.join(__location__, "definitelyNotWhereYourPasswordsAreStored.json"), "wb") as f:
        f.write(b'')

    cprint("\nSuccessfully set master password. Now run manager.py to use the password manager\n", "green")
