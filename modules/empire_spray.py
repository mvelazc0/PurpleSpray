#!/usr/bin/env python

# AUTHOR OF MODULE NAME
AUTHOR="Mauricio Velazco (@mvelazco)"

# DESCRIPTION OF THE MODULE
DESCRIPTION="This module simulates an adversary leveraging a compromised host to perform password spray attacks."

LONGDESCRIPTION="This scenario can occur if an adversary has obtained control of a domain joined computer through a --spear phishing attack or any other kind of client side attack.--Spray_empire leverages the Powershell Empire framework and its API to instruct Empire agents--to perform password spray attacks by using Invoke-SMBLogin (https://github.com/mvelazc0/Invoke-SMBLogin).--The module will connect to the Empire server and leverage existing agents. If no agents are found,--it will use impackets wmiexec to execute an Empire stager on a remote host defined on the settings."

# TODO
OPTIONS="""{"Dc": {"Description": "Domain Controller Ip address", "Required": "True", "Value": ""}, "Domain": {"Description": "Root domain name ( org.com )", "Required": "True", "Value": ""}, "Username": {"Description": "Domain user for ldap queries", "Required": "True", "Value": ""}, "Password": {"Description": "Domain user password for ldap queries", "Required": "True", "Value": ""}, "DomainUsers": {"Description": "Use domain users to spray. If False, random usernames will be used", "Required": "True", "Value": "True"}, "Nusers": {"Description": "Number of domain users to spray", "Required": "True", "Value": "10"}, "Type": {"Description": "Type of simulation", "Required": "True", "Value": "0"}, "UseKerberos": {"Description": "Kerberos or NTLM", "Required": "True", "Value": "True"}, "SprayPassword": {"Description": "Password used to spray", "Required": "True", "Value": "Winter2019"}}"""

ADVANCED_OPTIONS="""{ "EmpireHost": {"Description": "Ip address of the Empire Server ", "Required": "True", "Value": ""}, "EmpirePort": {"Description": "Rest API port number", "Required": "True", "Value": "1337"}, "EmpirePassword": {"Description": "Empire Rest API Password", "Required": "True", "Value": ""} ,"SimulationHost": {"Description": "Ip address of the simulation host", "Required": "False", "Value": ""}, "SimulationUser": {"Description": "Used against the simulation host. Requires admin privs", "Required": "False", "Value": ""} , "SimulationPass": {"Description": "Used against the simulation hos", "Required": "False", "Value": ""}, "Sleep": {"Description": "Time to sleep between each authentication attempt", "Required": "True", "Value": "0"} }"""

TYPES="""{"0": {"Description": "Perform the spray against a randomly picked domain controller"},"1": {"Description": "Perform the spray against a randomly picked domain computer "} , "2": {"Description": "Perform the spray against randomly picked domain computers. One auth per computer"}}"""