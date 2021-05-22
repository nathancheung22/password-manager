# methods to read, add, & remove passwords and shit
from getpass import getpass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import json
import pyperclip
import os
from colors import cprint

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def getAndConfirmPassword():
    password = getpass(prompt="Enter password: ")
    password2 = getpass(prompt="Confirm password: ")

    while password != password2:
        cprint("\nError: Passwords did not match\n", "red")
        password = getpass(prompt="Enter password: ")
        password2 = getpass(prompt="Confirm password: ")

    return password


def updateFile(passwordDict, f):
    jsonString = json.dumps(passwordDict).encode()
    encrypted = f.encrypt(jsonString)

    with open(os.path.join(__location__, "definitelyNotWhereYourPasswordsAreStored.json"), "wb") as file:
        file.write(encrypted)


def addPassword(passwordDict, f):
    listApps(passwordDict, f)

    app = input("Enter app name: ")

    if app in passwordDict:
        cprint("\nWarning: App already exists\n", "yellow")
    else:
        url = input("Enter website url: ")
        user = input("Enter email / username: ")
        password = getAndConfirmPassword()

        passwordDict[app] = {"url": url, "user": user, "password": password}
        updateFile(passwordDict, f)


def removePassword(passwordDict, f):
    listApps(passwordDict, f)

    app = input("Enter app name: ")

    if app in passwordDict:
        del passwordDict[app]
        updateFile(passwordDict, f)
    else:
        cprint("\nError: App doesn't exist\n", "red")


def changePassword(passwordDict, f):
    listApps(passwordDict, f)

    app = input("Enter app name: ")

    if app in passwordDict:
        password = getAndConfirmPassword()

        passwordDict[app]["password"] = password
        updateFile(passwordDict, f)

        cprint(f"\nPassword successfully changed for {app}", "green")
    else:
        cprint("\nError: App doesn't exist\n", "red")


def viewPassword(passwordDict, f):
    listApps(passwordDict, f)

    app = input("Enter app name: ")

    if app in passwordDict:
        url = passwordDict[app]["url"]
        user = passwordDict[app]["user"]
        password = passwordDict[app]["password"]

        print("""
        ------------- DETAILS -------------
        App name   | {}
        Url        | {}
        Username   | {}
        Password   | {}
        ------------- DETAILS -------------
        """.format(app, url, user, password))
    else:
        cprint("\nError: App doesn't exist\n", "red")


def copyPassword(passwordDict, f):
    listApps(passwordDict, f)

    app = input("Enter app name: ")

    if app in passwordDict:
        password = passwordDict[app]["password"]
        pyperclip.copy(password)

        cprint("\nPassword copied to clipboard\n", "green")
    else:
        cprint("\nError: App doesn't exist\n", "red")


def listApps(passwordDict, f):
    apps = "\n        ".join([app for app in passwordDict.keys()])
    apps = "No existing apps" if len(apps) == 0 else apps

    print("""
        --------------- EXISITING APPS ---------------
        {}
        --------------- EXISITING APPS ---------------
    """.format(apps))


def quit(passwordDict, f):
    cprint("\nThanks for using urvianoob's Password Manager v1.1!\n", "header")


def getFernetKey(password):
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        iterations=100000,
        backend=backend,
        salt=b'\xfe\xfbU\xdb\xab\x8f\x96-\x86\xc8\xc2\xa0L\xb7\xed\x8e'
    )

    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    f = Fernet(key)

    return f


