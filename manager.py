from getpass import getpass
import bcrypt
from methods import *
import json

try:
    with open("password.txt", "rb") as f:
        masterPasswordHash = f.read()
except FileNotFoundError:
    print("Manager not setup, please run setup.py")


print("\nurvianoob's Password Manager v1.0\n")
userPassword = getpass(prompt="Please enter the master password: ")

while not bcrypt.checkpw(userPassword.encode(), masterPasswordHash):
    print("\nError: Incorrect password \n")
    userPassword = getpass(prompt="Please enter the master password: ")

# creates encryption key stuff
f = getFernetKey(password=userPassword)

# decrypts and loads allPasswords into dict object
with open("definitelyNotWhereYourPasswordsAreStored.json", "rb") as file:
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

    selection = input("Enter your selection: ").lower()

    try:
        options[selection](passwordDict, f)
    except KeyError:
        print("\nError: Invalid selection\n")

