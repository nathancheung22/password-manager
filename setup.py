import bcrypt
from getpass import getpass

# shameless plug
print("\nurvianoob's Password Manager v1.0\n")

try:
    # if you have these files, then you've already run the setup
    with open("password.txt", "rb") as f:
        f.read()
    with open("definitelyNotWhereYourPasswordsAreStored.json", "rb") as f:
        f.read()

    print("Error: you've already setup the password-manager\n")

except FileNotFoundError:
    # if files not found, run the setup
    print("Welcome to the initial setup\n")

    password = getpass(prompt="Enter your master password: ")
    confirmPassword = getpass(prompt="Confirm your master password: ")
    while password != confirmPassword or len(password) < 15:
        if len(password) < 15:
            print("\nPlease enter a password that's 15 characters or longer")
        else:
            print("\nError: passwords did not match\n")

        password = getpass(prompt="Enter your master password: ")
        confirmPassword = getpass(prompt="Confirm your master password: ")

    x = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    with open("password.txt", "wb") as f:
        f.write(x)

    with open("definitelyNotWhereYourPasswordsAreStored.json", "wb") as f:
        f.write(b'')
