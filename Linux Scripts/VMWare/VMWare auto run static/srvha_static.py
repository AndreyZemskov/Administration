"""
    Before use script you should install the next librory:
    pip install paramiko
    pip install pyyaml
    pip install cryptography==2.4.2 or later version
    or you can use requirements file, for example
    pip install -r requirements.txt

"""

import subprocess
import time
import paramiko
import yaml

""" 
    Parameters of authentications
    which are located in mp.yaml file 
"""
mp = yaml.load(open('mp.yaml'))
server = mp['server']
port = mp['port']
user = mp['user']
password = mp['password']
command = 'vim-cmd vmsvc/power.on <vmID>' # This command start up VM in remote host

def SSHClient(server, port, user, password):
    """ This function creating to connection """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    print('Client was created')
    return client

def ssh_cli(client, command):
    """
        This function creating to secure tunnel
        across an SSH Transport
    """
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)
    channel.exec_command(command)
    # channel.send(password+'\n')
    print('Session was opened')
    print(channel.recv(1024))
    client.close()
    channel.close()

hostname = 'IP or Hostname'
response = subprocess.call(['ping', hostname]) # This command listening port in remote machine
print(response)

if response == 0:
    print(hostname, "is up")
elif response == 1:
    print(hostname, "is down")
    time.sleep(60)
    ssh_cli(SSHClient(server, port, user, password), command)
    print('Command was sended')


