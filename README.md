# Password Manager

Why pay for lastpass when you can make it yourself.
Feel free to submit pull requests, especially if you see any critical errors 😀

### How effective is this?
- The master password is stored as a hash with a randomly generated salt value attached to it. It uses an algorithm based on the Blowfish cipher, and is the default algorithm for OpenBSD
- The file where your passwords are stored is encrypted with your actual password hashed using SHA256, with a predefined salt and and 100,000 iterations

### How can I trust this?
- It's open source
- However, I'm no security expert so you probably can't

### Possible flaws
- If somehow the masterpassword hash could be converted to the encryption key hash, this would break the system
- Quantum computing

