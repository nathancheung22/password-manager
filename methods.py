# methods to read, add, & remove passwords and shit
from getpass import getpass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import json


def getAndConfirmPassword():
    password = getpass(prompt="Enter password: ")
    password2 = getpass(prompt="Confirm password: ")

    while password != password2:
        print("\nPASSWORDS DID NOT MATCH\n")
        password = getpass(prompt="Enter password: ")
        password2 = getpass(prompt="Confirm password: ")

    return password


def updateFile(passwordDict, f):
    jsonString = json.dumps(passwordDict).encode()
    encrypted = f.encrypt(jsonString)

    with open("definitelyNotPasswords.json", "wb") as file:
        file.write(encrypted)


def addPassword(passwordDict, f):
    app = input("Enter app name: ")
    while app in passwordDict:
        app = input("ALREADY EXISTS! Enter app name: ")
    
    url = input("Enter website url: ")
    user = input("Enter email / username: ")
    password = getAndConfirmPassword()

    passwordDict[app] = {"url": url, "user": user, "password": password}
    updateFile(passwordDict, f)


def removePassword(passwordDict, f):
    app = input("Enter app name: ")
    while app not in passwordDict:
        app = input("DOESN'T EXISTS! Enter app name: ")

    del passwordDict[app]
    updateFile(passwordDict, f)


def changePassword(passwordDict, f):
    app = input("Enter app name: ")
    while app not in passwordDict:
        print("\nError: App doesn't exist\n")
        app = input("Enter app name: ")

    password = getAndConfirmPassword()

    passwordDict[app]["password"] = password
    updateFile(passwordDict, f)


def viewPassword(passwordDict, f):
    app = input("Enter app name: ")
    while app not in passwordDict:
        print("\nError: App doesn't exist\n")
        app = input("Enter app name: ")

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


def quit(passwordDict, f):
    exit()


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


