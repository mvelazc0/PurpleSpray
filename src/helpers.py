import socket
import random
import dns.resolver
import string
from src.core import print_failed_auth, print_succ_auth


def generate_random_users(size):

    users=[]
    for i in range(0,size):
        users.append(''.join(random.choice(string.ascii_lowercase) for _ in range(10)))

    return users

def get_live_hosts(domain, hosts, dc_ip):

    hosts = get_resolvable_hosts(domain, hosts, dc_ip)
    hosts = get_smb_hosts(hosts)
    return hosts

def get_resolvable_hosts(domain, computers, dc_ip):

    hosts_alive=[]
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dc_ip]
    for pc in computers:
        pc = pc.replace("$","")
        pc = pc+"."+domain
        #print ("trying to resolve", pc , " against:"+dc_ip)
        try:
            answer=resolver.query(pc)
            hosts_alive.append([pc,answer[0].address])
            #print (pc, " has an ip!")
        except Exception as e:
            #print (e)
            #print ("pc", "not resolvable")
            pass
    return hosts_alive

def get_smb_hosts(computers):

    socket.setdefaulttimeout(2)
    smb_alive=[]
    for pc in computers:
        #print ("trying to connect to 445 to ",str(pc[1]))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((pc[1],445))
            s.close()
            smb_alive.append(pc)
            #print ("port open on",pc[1])
        except Exception as e:
            #print (e)
            #print ("port closed on ", pc[1])
            pass

    socket.setdefaulttimeout(None)
    return smb_alive

def process_empire_results(results,host):

    for res in results.splitlines():
        if 'ComputerName' not in res and '--' not in res and 'Invoke' not in res and len(res)>1:
            auth_result=res.split()
            if (len(auth_result) == 4 and auth_result[3] == 'Success'):
                print_succ_auth("", auth_result[1], auth_result[2], host)
            elif (len(auth_result) == 4 and auth_result[3] == 'Failed'):
                print_failed_auth("", auth_result[1], auth_result[2], host)