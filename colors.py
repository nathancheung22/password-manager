class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cprint(text, color):
    colordict = {
        "cyan": bcolors.OKCYAN,
        "blue": bcolors.OKBLUE,
        "green": bcolors.OKGREEN,
        "yellow": bcolors.WARNING,
        "red": bcolors.FAIL,
        "header": bcolors.HEADER,
        "bold": bcolors.BOLD,
        "underline": bcolors.UNDERLINE
    }

    ccolor = colordict[color]

    print(f"{ccolor}{text}{bcolors.ENDC}")