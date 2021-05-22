from getpass import getpass
import bcrypt
from methods import *
import json
import os
import sys
from colors import cprint


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

try:
    with open(os.path.join(__location__, "password.txt"), "rb") as f:
        masterPasswordHash = f.read()
except FileNotFoundError:
    cprint("Manager not setup, please run setup.py", "red")
    sys.exit(1)


cprint("\nurvianoob's Password Manager v1.1\n", "header")
userPassword = getpass(prompt="Please enter the master password: ")

while not bcrypt.checkpw(userPassword.encode(), masterPasswordHash):
    cprint("\nError: Incorrect password \n", "red")
    userPassword = getpass(prompt="Please enter the master password: ")

# creates encryption key stuff
f = getFernetKey(password=userPassword)

# decrypts and loads allPasswords into dict object
with open(os.path.join(__location__, "definitelyNotWhereYourPasswordsAreStored.json"), "rb") as file:
    data = file.read()
    if data == b'':
        passwordDict = {}
    else:
        decryptedData = f.decrypt(data).decode("utf-8")
        passwordDict = json.loads(decryptedData)

# now we're logged in
selection = ""
while selection != "q":
    options = {
        '1': addPassword,
        '2': removePassword,
        '3': changePassword,
        '4': viewPassword,
        '5': listApps,
        '6': copyPassword,
        'q': quit
    }

    print("""
        --------------- MENU ---------------
        1: Add password
        2: Remove password
        3: Change password
        4: View password
        5: List apps
        6: Copy password
        Q: Quit
        --------------- MENU ---------------
    """)

    selection = input("Menu selection: ").lower()

    try:
        options[selection](passwordDict, f)
    except KeyError:
        print("\nError: Invalid selection\n")
