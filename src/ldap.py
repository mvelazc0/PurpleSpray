import sys
sys.path.append("../")
from lib.getadusers import GetADUsers

def get_users(username, password, domain, dc_ip):

    #(username, password, domain, aesKey=None, useKerberos=False, hashes=None, dc_ip, objectType):
    executer = GetADUsers(username, password, domain,dc_ip, "user",aesKey=None,useKerberos=False,hashes=None, )
    users = executer.run()
    results=[]
    for u in users:
        try:
            newuser=(u._componentValues[1]._componentValues[2]._componentValues[1]._componentValues[0]._value).decode("utf-8")
            if newuser != "Guest" and newuser != "krbtgt":
                results.append(newuser)
        except:
            pass
    return results

def get_dcs(username, password, domain, dc_ip):

    #(username, password, domain, aesKey=None, useKerberos=False, hashes=None, dc_ip, objectType):
    executer = GetADUsers(username, password, domain,dc_ip, "dc",aesKey=None,useKerberos=False,hashes=None, )
    dcs = executer.run()
    results=[]
    for dc in dcs:
        try:
            newdc=(dc._componentValues[1]._componentValues[2]._componentValues[1]._componentValues[0]._value).decode("utf-8")
            results.append(newdc)
        except:
            pass


    return results

def get_computers(username, password, domain, dc_ip):

    #(username, password, domain, aesKey=None, useKerberos=False, hashes=None, dc_ip, objectType):
    executer = GetADUsers(username, password, domain,dc_ip, "computer",aesKey=None,useKerberos=False,hashes=None, )
    computers = executer.run()
    results=[]
    for c in computers:

        try:
            newpc=(c._componentValues[1]._componentValues[2]._componentValues[1]._componentValues[0]._value).decode("utf-8")
            results.append(newpc)
        except Exception as e:
            pass

    return results

