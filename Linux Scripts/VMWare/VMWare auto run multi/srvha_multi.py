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
    which are located in mp.yaml file.
"""

mp = yaml.load(open('mp.yaml'))
port = mp['port']
user = mp['user']
password = mp['password']

def SSHClient(server, port, user, password):
    """ This function creating to connection. """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    print('Client was created')
    return client

def ssh_cli(client, command):
    """
        This function creating to secure tunnel
        across an SSH Transport.
    """
    channel = client.get_transport().open_session()
    channel.get_pty()
    channel.settimeout(5)
    channel.exec_command(command)
    print('Session was opened')
    print(channel.recv(1024))
    client.close()
    channel.close()

""" List of accordance ESXI host and VM. """
for vsm in yaml.load_all(open('vrt_srv_mapping.yaml')):
    vsmap = vsm

""" List of accordance VM and commands. """
for cmd in yaml.load_all(open('vmid_cmd.yaml')):
    vmid = cmd

def flow():
    """
        This function listening network interfaces on remote machine.
        If connection is lost will be send command on match VM in other ESXI host.

    """
    while True:
        try:
            for vrt, srv in vsmap.items():
                response = subprocess.call(['ping', '-c', '3', vrt]) # This command listening port in remote machine
                if response == 0:
                    print(vrt, "is up")
                elif response == 1:
                    print(vrt, "is down")
                    time.sleep(5)
                    for vm, cmd in vmid.items():
                        if vm == vrt:
                            ssh_cli(SSHClient(srv, port, user, password), cmd)
                            print('Command was sended')
        except TimeoutError:
            print('Connection timed out')
            continue

if __name__ == '__main__':
    flow()
