#!/usr/bin/env python
import os

import glob
import platform
import sys

# tab completion
def complete(text, state):
    a = (glob.glob(text + '*') + [None])[state].replace("__init__.py", "").replace(".py", "").replace("LICENSE", "").replace(
        "README.md", "").replace("config", "").replace("ptf", "").replace("readme", "").replace("src", "").replace("         ", "") + "/"
    a = a.replace("//", "/")
    if os.path.isfile(a[:-1] + ".py"):
        return a[:-1]
    else:
        return a

# if running on linux
if platform.system() != "Windows":
    import readline
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
# end tab completion

# color scheme for core


class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERL = '\033[4m'
    ENDC = '\033[0m'
    backBlack = '\033[40m'
    backRed = '\033[41m'
    backGreen = '\033[42m'
    backYellow = '\033[43m'
    backBlue = '\033[44m'
    backMagenta = '\033[45m'
    backCyan = '\033[46m'
    backWhite = '\033[47m'
# get the main SET path
def definepath():
    if os.path.isfile("ptf"):
        return os.getcwd()

    else:
        if os.path.isdir("/usr/share/ptf/"):
            return "/usr/share/ptf/"
        else:
            return os.getcwd()

# main status calls for print functions
def print_status(message):
    print((bcolors.GREEN) + (bcolors.BOLD) + \
        ("[*] ") + (bcolors.ENDC) + (str(message)))


def print_info(message):
    print((bcolors.BLUE) + (bcolors.BOLD) + \
        ("[-] ") + (bcolors.ENDC) + (str(message)))


def print_info_spaces(message):
    print((bcolors.BLUE) + (bcolors.BOLD) + \
        ("  [-] ") + (bcolors.ENDC) + (str(message)))


def print_warning(message):
    print((bcolors.YELLOW) + (bcolors.BOLD) + \
        ("[!] ") + (bcolors.ENDC) + (str(message)))

def print_failed_auth(domain, user, password, target):

    if domain != "":
        print((bcolors.RED) + (bcolors.BOLD) + ("\t[-] ") + (bcolors.ENDC) + (str(domain + "\\" + user + ":" + password+"@ "+target[0]+" ("+target[1]+")")))
    else:
        print((bcolors.RED) + (bcolors.BOLD) + ("\t[-] ") + (bcolors.ENDC) + (user + ":" + password +" @ "+target[0]+" ("+target[1]+")"))

def print_succ_auth(domain, user, password, target):
    if domain != "":
        print((bcolors.GREEN) + (bcolors.BOLD) + ("\t[*] ") + (bcolors.ENDC) + (str(domain + "\\" + user + ":" + password+" @ "+target[0]+" ("+target[1]+")" )))
    else:
        print((bcolors.GREEN) + (bcolors.BOLD) + ("\t[*] ") + (bcolors.ENDC) + (user + ":" + password +" @ "+target[0]+" ("+target[1]+")"))

def print_error(message):
    print((bcolors.RED) + (bcolors.BOLD) + \
        ("[!] ") + (bcolors.ENDC) + (bcolors.RED) + \
        (str(message)) + (bcolors.ENDC))

def set_title(title):
	sys.stdout.write("\x1b]2;%s\x07" % title)


# version information
grab_version = "1.0"

# banner
banner = bcolors.PURPLE + r"""

    ______                 _      _____                       
    | ___ \               | |    /  ___|                      
    | |_/ /   _ _ __ _ __ | | ___\ `--. _ __  _ __ __ _ _   _ 
    |  __/ | | | '__| '_ \| |/ _ \`--. \ '_ \| '__/ _` | | | |
    | |  | |_| | |  | |_) | |  __/\__/ / |_) | | | (_| | |_| |
    \_|   \__,_|_|  | .__/|_|\___\____/| .__/|_|  \__,_|\__, |
                    | |                | |               __/ |
                    |_|                |_|              |___/ 

"""
banner += """        		   """ + bcolors.backBlue + \
    """v1.0"""+ bcolors.ENDC + "\n"

banner += """           		 by: """ + bcolors.BOLD + \
    """Mauricio Velazco (@mvelazco)""" + bcolors.ENDC + "\n"

banner += """
PurpleSpray is an adversary simulation tool that executes password
spray behavior  under different scenarios and conditions within 
Windows enterprise environments. Purple teams can leverage PurpleSpray 
to identify gaps in visibility as well as build, test and improve 
detection analytics for spraying attacks.
"""

def module_options(filename,term):

    if os.path.isfile(filename) and ".py" in filename and not ".pyc" in filename:
        # open the file
        fileopen = open(filename, "r")
        # iterate through the file
        for line in fileopen:
            # strip any bogus stuff
            line = line.rstrip()
            # if the line starts with the term
            if line.startswith(term):
                line = line.replace(term + '=', "")
                line = line.replace('"""', "")
                # reflect we hit this and our search term was found
                return line



    if not os.path.isfile(filename):
        return None

def module_parser(filename, term):
    # if the file exists
    if os.path.isfile(filename) and ".py" in filename and not ".pyc" in filename:

        # set a base counter
        counter = 0

        # open the file
        fileopen = open(filename, "r")
        # iterate through the file
        for line in fileopen:
            # strip any bogus stuff
            line = line.rstrip()
            # if the line starts with the term
            if line.startswith(term):
                line = line.replace(term + '="', "")
                line = line.replace(term + "='", "")
                line = line.replace(term + "=", "")
                if str(line).endswith('"'): line = line[:-1]
                if str(line).endswith("'"): line = line[:-1]
                # reflect we hit this and our search term was found
                counter = 1
                return line

    # if the file isn't there
    if not os.path.isfile(filename):
        return None

# help menu
def show_help_menu():
    print(("Available from main prompt: " + bcolors.BOLD + "show modules" + bcolors.ENDC + "," + bcolors.BOLD + " show <module>" +
           bcolors.ENDC + "," + bcolors.BOLD + " use <module>" + bcolors.ENDC))
    print(("Inside modules:" + bcolors.BOLD + " show options" + bcolors.ENDC + bcolors.BOLD + " show advanced" + bcolors.ENDC +"," +
           bcolors.BOLD + " set <option>" + bcolors.ENDC + "," + bcolors.BOLD + "run" + bcolors.ENDC))
    print(("Additional commands: " + bcolors.BOLD + "back" + bcolors.ENDC + "," + bcolors.BOLD + " help" + bcolors.ENDC + "," +
           bcolors.BOLD + " ?" + bcolors.ENDC + "," + bcolors.BOLD + " exit" + bcolors.ENDC + "," + bcolors.BOLD + " quit" + bcolors.ENDC))
    print(("empire_spray module: " + bcolors.BOLD + "initialize" + bcolors.ENDC + "," + bcolors.BOLD + " stagers" + bcolors.ENDC))

# exit message
def exit_ps():
    print_status("Exiting PurpleSpray - Happy Purple Teaming!.")

