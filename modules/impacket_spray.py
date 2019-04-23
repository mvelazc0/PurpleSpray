#!/usr/bin/env python

# AUTHOR OF MODULE NAME
AUTHOR="Mauricio Velazco (@mvelazco)"

# DESCRIPTION OF THE MODULE
DESCRIPTION="This module simulates an adversary leveraging a rogue device to perform password spray attacks."

LONGDESCRIPTION="This scenario can occur if an adversary has direct access to the network through physical access --or an unauthorized VPN connection and uses a non domain joined device to execute --the attacks. Spray_impacket leverages the impacket library to perform the spray attacks."

# TODO
OPTIONS="""{"Dc": {"Description": "Domain Controller Ip address", "Required": "True", "Value": ""}, "Domain": {"Description": "Root domain name ( org.com )", "Required": "True", "Value": ""}, "Username": {"Description": "Domain user for ldap queries", "Required": "True", "Value": ""}, "Password": {"Description": "Domain user password for ldap queries", "Required": "True", "Value": ""}, "DomainUsers": {"Description": "Use domain users to spray. If False, random usernames will be used.", "Required": "True", "Value": "True"}, "Nusers": {"Description": "Number of domain users to spray", "Required": "True", "Value": "10"}, "Type": {"Description": "Type of simulation", "Required": "True", "Value": "0"} , "SprayPassword": {"Description": "Password used to spray", "Required": "True", "Value": "Winter2019"}}"""

ADVANCED_OPTIONS="""{"Sleep": {"Description": "Time to sleep between each authentication attempt", "Required": "True", "Value": "0"} }"""

TYPES="""{"0": {"Description": "Perform the spray against a randomly picked domain controller"},"1": {"Description": "Perform the spray against a randomly picked domain computer "} , "2": {"Description": "Perform the spray against randomly picked domain computers. One auth per computer"}}"""