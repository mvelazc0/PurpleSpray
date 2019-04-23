from impacket.smbconnection import SMBConnection, SMB_DIALECT, SMB2_DIALECT_002, SMB2_DIALECT_21
from src.core import print_failed_auth, print_succ_auth
import time

def impacket_smb_login(domain, user, password, target):
    try:
        smbConnection = SMBConnection(target[0], target[1])
        # smbConnection.login(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)
        smbConnection.login(user, password,domain)
        #print("auth success !!")
        print_succ_auth(domain, user, password, target)

    except Exception as e:
        #print(e)
        print_failed_auth(domain, user, password, target)
        #print("auth failed")



def smb_login(domain, users, password, target, sleep):

    users = users.split() if type(users) is not list else users
    for user in users:
        impacket_smb_login(domain, user, password, target)
        if sleep > 0 :
            time.sleep(sleep)


def mass_smb_login(domain, users, passwords, targets):

    targets=targets.split() if type(targets) is not list else targets
    for target in targets:
        users = users.split() if type(users) is not list else users
        for user in users:
            passwords= passwords.split() if type(passwords) is not list else passwords
            for password in passwords:
                #print("tryng user:",user," domain:",domain," password:",password," against target:",target)
                impacket_smb_login(domain, user, password, target)

