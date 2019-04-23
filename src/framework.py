#!/usr/bin/env python
#
#

from src.core import *
from src.empire import EmpireSession
import platform
import os
import json
from src.spray import *
from src.rce import execute_stager
import time

import traceback

# if running on linux
if platform.system() != "Windows":
    import readline

# python 2 compatibility
try: input = raw_input
except NameError: pass

# print the main welcome banner
print (banner)

print ("""For a list of available commands type ? or help\n""")


def show_module():
    width=30
    modules_path = os.getcwd() + "/modules/"
    print ("\n")
    print((bcolors.BOLD + "PurpleSpray Modules" + bcolors.ENDC))
    print("""=================================\n""")
    print((bcolors.BOLD) + ("""  Name"""+(width-len("Name"))*' '+"""Description """) + (bcolors.ENDC))
    print("""  ----"""+(width-len("Name"))*' '+"""---------------""")
    for path, subdirs, files in os.walk(modules_path):
        for name in sorted(files):
            # join the structure
            filename = os.path.join(path, name)
            # strip un-needed files
            if not name in ('__init__.py'):
                # shorten it up a little bit
                filename_short = filename.replace(os.getcwd() + "/", "")
                filename_short = filename_short.replace(".py", "")
                filename_short = str(filename_short)
                description = module_parser(filename, "DESCRIPTION")
                # print the module name
                if description != None:
                    temp_number = width - len(filename_short)
                    print("  "+filename_short + " " * temp_number + description)
    print("\n")

# this is when a use <module> command is initiated
def use_module(module):
    prompt = ("")
    # if we aren't using all
    if not "__init__" in module:

        # set terminal title
        set_title("PurpleSpray - %s" % module)

        filename = definepath() + "/" + module + ".py"

        # grab the author
        try:
            author = module_parser(filename, "AUTHOR")

        except TypeError:
            author = "Invalid"

        # grab the description
        description = module_parser(filename, "DESCRIPTION")

        # grab the description
        longdescription = module_parser(filename, "LONGDESCRIPTION")

        options = json.loads(module_options(filename,"OPTIONS"))

        otheroptions=module_options(filename, "OTHER_OPTIONS")
        if otheroptions:
            otheroptions = json.loads(otheroptions)

        typeoptions=module_options(filename,"TYPES")
        if typeoptions:
            typeoptions = json.loads(typeoptions)

        advanceddoptions = module_options(filename,"ADVANCED_OPTIONS")
        if advanceddoptions:
            advanceddoptions = json.loads(advanceddoptions)

        ActiveAgent = False
        empireagent=None
        empiresession=None


        while 1:

            try:
                prompt = input(bcolors.BOLD + "PurpleSpray:" + bcolors.ENDC +
                                   "(" + bcolors.PURPLE + "%s" % module + bcolors.ENDC + ")>")
            except EOFError:
                prompt = "back"
                print("")

            # exit if we need to
            if prompt == "back" or prompt == "quit" or prompt == "exit":
                return "None"

            # show the help menu
            if prompt == "?" or prompt == "help":
                show_help_menu()

            # show modules
            if prompt == "show modules":
                print_warning(
                    "In order to show modules, you must type 'back' first")

            # if we are using a module within a module we return our prompt
            if "use " in prompt:
                return prompt

            if prompt.lower() == "info":
                print("\n")
                print(
                    bcolors.BOLD + "Module Author:         " + bcolors.ENDC + author)
                print(
                    bcolors.BOLD + "Module Description:    " + bcolors.ENDC + description)

                print(bcolors.BOLD + "Long Description:      " + bcolors.ENDC+ longdescription.replace('-','\n').splitlines()[0] )

                for line in longdescription.replace('--','\n').splitlines( )[1:]:
                    print (" "*23 + line)

                print("\n")


            # options menu - was a choice here to load upon initial load of dynamically pull each time
            if prompt.lower() == "show options":
                gwidth=17
                print("Module options (%s):" % module)

                print("\n")

                print(bcolors.BOLD + "  Name" + ' ' * (gwidth - len("Name")) + "Value" + ' ' * (gwidth - len("Value")) + "Description" + ' ' * (gwidth - len("Description")) + bcolors.ENDC)
                print(
                    bcolors.BOLD + "  ----" + ' ' * (gwidth - len("Name")) + "-----" + ' ' * (gwidth - len("Value")) + "-----------" + ' ' * (gwidth - len("Description")) + bcolors.ENDC)
                for key in options.keys():
                    if not options[key]['Value']:

                        print("  "+key + ' ' * (gwidth - len(key)) + options[key]['Value'] + ' ' * (gwidth) +options[key]['Description'])
                    else:
                        print("  "+key + ' ' * (gwidth - len(key)) + options[key]['Value'] + ' ' * (gwidth - len(options[key]['Value'])) + options[key]['Description'])
                print("\n")

                if typeoptions:
                    gwidth2 = 7
                    print(bcolors.BOLD + "  Type" + ' ' * (gwidth2 - len("Type")) + "Description" + ' ' * (gwidth2 - len("Description")) + bcolors.ENDC)
                    print(bcolors.BOLD + "  ----" + ' ' * (gwidth2 - len("Type")) +  "-----------" + ' ' * (gwidth2 - len("Description")) + bcolors.ENDC)

                    for key in sorted(typeoptions.keys()):
                        print("  "+key + ' ' * (gwidth2 - len(key)) + typeoptions[key]['Description'])

                    print("\n")

                if otheroptions:
                    print(bcolors.BOLD + "  Name" + ' ' * (gwidth - len("Name")) + "Value" + ' ' * (
                            gwidth - len("Value")) + "Description" + ' ' * (
                                  gwidth - len("Description")) + bcolors.ENDC)
                    # print(bcolors.BOLD+"----"+ ' ' * 18+ "--------"+ ' ' * 14+ "-----"+ ' ' * 17+ "-----------"+ ' ' * 11+bcolors.ENDC)
                    print(
                        bcolors.BOLD + "  ----" + ' ' * (gwidth - len("Name")) + "-----" + ' ' * (
                                gwidth - len("Value")) + "-----------" + ' ' * (
                                gwidth - len("Description")) + bcolors.ENDC)
                    for key in sorted(otheroptions.keys()):

                        if not otheroptions[key]['Value']:

                            print("  "+
                                key + ' ' * (gwidth - len(key)) + otheroptions[key]['Value'] + ' ' * (gwidth) + otheroptions[key][
                                    'Description'])
                        else:

                            print("  "+key + ' ' * (gwidth - len(key)) + otheroptions[key]['Value'] + ' ' * (
                                        gwidth - len(otheroptions[key]['Value'])) + otheroptions[key]['Description'])
                    print("\n")

            if prompt.lower() == "show advanced":
                gwidth = 17
                print("Advanced module options for (%s):" % module)

                print("\n")

                print(bcolors.BOLD + "  Name" + ' ' * (gwidth - len("Name")) + "Value" + ' ' * (
                            gwidth - len("Value")) + "Description" + ' ' * (gwidth - len("Description")) + bcolors.ENDC)

                print(
                    bcolors.BOLD + "  ----" + ' ' * (gwidth - len("Name")) + "-----" + ' ' * (
                                gwidth - len("Value")) + "-----------" + ' ' * (
                                gwidth - len("Description")) + bcolors.ENDC)
                for key in advanceddoptions.keys():
                    if not advanceddoptions[key]['Value']:

                        print("  "+key + ' ' * (gwidth - len(key)) + advanceddoptions[key]['Value'] + ' ' * (gwidth) + advanceddoptions[key][
                            'Description'])
                    else:

                        print("  "+key + ' ' * (gwidth - len(key)) + advanceddoptions[key]['Value'] + ' ' * (
                                    gwidth - len(advanceddoptions[key]['Value'])) + advanceddoptions[key]['Description'])
                print("\n")
                # print("-------------------------------------------------------------------------------------")

            # if we are setting the command now
            if prompt.lower().startswith("set"):
                # need to grab the options
                set_breakout = prompt.split(" ")
                # here we rewrite the options for the menu
                if set_breakout[1].upper() == "USERNAME":
                    options['Username']['Value']= set_breakout[2]
                if set_breakout[1].upper() == "PASSWORD":
                    options['Password']['Value']= set_breakout[2]
                if set_breakout[1].upper() == "DOMAIN":
                    options['Domain']['Value']= set_breakout[2]
                if set_breakout[1].upper() == "DC":
                    options['Dc']['Value']= set_breakout[2]
                if set_breakout[1].upper() == "SPRAYPASSWORD":
                    options['SprayPassword']['Value']= set_breakout[2]
                if set_breakout[1].upper() == "NUSERS":
                    if set_breakout[2].isdigit() and int(set_breakout[2]) < 21 :
                        # PurpleSpray is not a red team tool :)
                        options['Nusers']['Value']= set_breakout[2]
                if set_breakout[1].upper() == "TYPE":
                    if set_breakout[2].isdigit() and int(set_breakout[2]) >=0 and int(set_breakout[2]) <=2 :
                        options['Type']['Value']= set_breakout[2]
                if set_breakout[1].upper() == "DOMAINUSERS" and set_breakout[2].upper() in ["TRUE","FALSE"]:
                    options['DomainUsers']['Value']= set_breakout[2]
                if set_breakout[1].upper() == "USEKERBEROS" and set_breakout[2].upper() in ["TRUE","FALSE"]:
                    options['UseKerberos']['Value']= set_breakout[2]

                if advanceddoptions:

                    if set_breakout[1].upper() == "EMPIREHOST":
                        advanceddoptions['EmpireHost']['Value'] = set_breakout[2]
                    if set_breakout[1].upper() == "EMPIREPASSWORD":
                        advanceddoptions['EmpirePassword']['Value'] = set_breakout[2]
                    if set_breakout[1].upper() == "EMPIREPORT":
                        advanceddoptions['EmpirePort']['Value'] = set_breakout[2]
                    if set_breakout[1].upper() == "SIMULATIONHOST":
                        advanceddoptions['SimulationHost']['Value'] = set_breakout[2]
                    if set_breakout[1].upper() == "SIMULATIONUSER":
                        advanceddoptions['SimulationUser']['Value'] = set_breakout[2]
                    if set_breakout[1].upper() == "SIMULATIONPASS":
                        advanceddoptions['SimulationPass']['Value'] = set_breakout[2]
                    if set_breakout[1].upper() == "SLEEP":
                        if set_breakout[2].isdigit():
                            advanceddoptions['Sleep']['Value'] = set_breakout[2]




            if prompt.lower() == "initialize":

                if "empire" in module:

                    empirehost = advanceddoptions['EmpireHost']['Value']
                    empirepassword = advanceddoptions['EmpirePassword']['Value']
                    empireport = advanceddoptions['EmpirePort']['Value']
                    simulationhost = advanceddoptions['SimulationHost']['Value']
                    victimusername = advanceddoptions['SimulationUser']['Value']
                    victimpassword = advanceddoptions['SimulationPass']['Value']


                    empsession = EmpireSession(empirehost, int(empireport), 'empireadmin', empirepassword)

                    if empsession.token['token']:

                        empsession.remove_stale_agents()
                        print_info("Checking for existing agents...")
                        agents = empsession.get_agents()['agents']
                        if len(agents) > 0:
                            print_status("Found active agent " + agents[0]['hostname'] + " (" + agents[0][
                                    'external_ip'] + ")" + ". Ready to spray!")

                            ActiveAgent = True
                            empireagent = agents[0]['name']
                            empiresession = empsession

                        else:
                            print_error("Did not identify existing agents.")

                            if simulationhost and victimusername and victimpassword:
                                print_info("Executing payload on simulation host...")
                                if len(victimusername.split("\\")) == 2:
                                    execute_stager(simulationhost, victimusername.split("\\")[1], victimpassword,victimusername.split("\\")[0], empsession)
                                else:
                                    execute_stager(simulationhost, victimusername, victimpassword, "", empsession)
                                print_info("Waiting up to 30 seconds for the shell .....")
                                time.sleep(30)
                                agents = empsession.get_agents()['agents']
                                if len(agents) > 0:
                                    print_status(
                                        "Succesfully obtained an Empire shell on " + agents[0]['hostname'] + " (" + agents[0][
                                            'external_ip'] + ")" + ". Ready to spray!")

                                    ActiveAgent=True
                                    empireagent=agents[0]['name']
                                    empiresession=empsession
                                else:
                                    print_error("Could not obtain shell :(. You may have to obtain an Empire shell manually")
                                    print_warning("Run the 'stagers' command to generate Empire stagers.")

                            else:
                                print_error("Information for the simulation host is required.")

            if prompt.lower() == "stagers":

                if "empire" in module:

                    empirehost = advanceddoptions['EmpireHost']['Value']
                    empirepassword = advanceddoptions['EmpirePassword']['Value']
                    empireport = advanceddoptions['EmpirePort']['Value']
                    empsession = EmpireSession(empirehost, int(empireport), 'empireadmin', empirepassword)

                    if empsession.token['token']:
                        print_warning("Generating Powershell Empire stagers...")
                        try:
                            empsession.generate_stagers()
                            print_status("Succesfully created the payloads under the 'stagers' folder.")
                        except:
                            pass
                            print(traceback.format_exc())
                    else:
                        pass







            if prompt.lower() == "run":
                try:
                    # RUN MODULE

                    if "impacket" in module:
                        username = options['Username']['Value']
                        domain = options['Domain']['Value']
                        password = options['Password']['Value']
                        spraypassword = options['SprayPassword']['Value']
                        dc_ip = options['Dc']['Value']
                        type = options['Type']['Value']
                        nusers = int(options['Nusers']['Value'])
                        sleep =  int(advanceddoptions['Sleep']['Value'])
                        UseDomainAct = eval(options['DomainUsers']['Value'])
                        impacket_spray(domain, username, password, dc_ip, nusers,sleep, UseDomainAct, spraypassword, type)

                    elif "empire" in module:

                        if ActiveAgent :
                            username = options['Username']['Value']
                            domain = options['Domain']['Value']
                            password = options['Password']['Value']
                            dc_ip = options['Dc']['Value']
                            type = options['Type']['Value']
                            sleep = int(advanceddoptions['Sleep']['Value'])
                            nusers = int(options['Nusers']['Value'])
                            spraypassword = options['SprayPassword']['Value']
                            UseDomainAct=eval(options['DomainUsers']['Value'])
                            useKerberos=eval(options['UseKerberos']['Value'])
                            empire_spray(empiresession,empireagent, domain, username, password, dc_ip, nusers, type, spraypassword, sleep, UseDomainAct,useKerberos)

                        else:
                            print_info("You first need to run the \'initialize\' command to run this module.")

                except Exception as e:
                    pass
                    print(traceback.format_exc())


                pass


def handle_prompt(prompt, force=False):
    # specify no commands, if counter increments then a command was found
    base_counter = 0

    # main help menu
    if prompt == "?" or prompt == "help":
        show_help_menu()
        base_counter = 1

    # if we want to exit out
    if prompt == "quit" or prompt == "exit" or prompt == "back":
        base_counter = 1
        exit_ps()
        sys.exit()

    # if we want to see the modules
    if prompt == "show modules":
        base_counter = 1
        show_module()

    # if we want to use a module
    if prompt.startswith("use"):
        base_counter = 1
        counter = 0
        prompt = prompt.split(" ")

        if os.path.isfile(definepath() + "/" + prompt[1] + ".py"):
            counter = 1

        if counter == 1:
            while 1:
                try:
                    module = use_module(prompt[1])
                    if "use " in module:
                        prompt = module.split(" ")
                    else: break
                except Exception as e:
                    print (e)
                    print(traceback.format_exc())
                    break

        if counter == 0:
            print_error("Module name was not found, try retyping it again.")

    # if blanks are used
    if prompt == "":
        base_counter = 1

    if base_counter == 0:
        print_warning(
            "Command was not found, try help or ? for more information.")

# start the main loop
def mainloop():

    while 1:
        # set title
        set_title("Purplespray v%s" % grab_version)

        try:
            prompt = input(bcolors.BOLD + "PurpleSpray" + bcolors.ENDC + "> ")
        except EOFError:
            prompt = "quit"
            print("")
        handle_prompt(prompt)
