"""
    Before use script you should install the next librory:
    pip install paramiko
    pip install pyyaml
    pip install cryptography==2.4.2 or later version
    or you can use requirements file, for example
    pip install -r requirements.txt

"""

import paramiko
import yaml

""" 
    Parameters of authentications
    which are located in mp.yaml file 
"""

mp = yaml.load(open('mp.yaml'))
port = mp['port']
user = mp['user']
password = mp['password']

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
    # channel.send(password+'\n') # If you want to run commands from another user uncomment this string
    print('Session was opened')
    print(channel.recv(1024))
    client.close()
    channel.close()

if __name__ == '__main__':
    for srv in open('servers.txt'):
        for cmd in open('commands_list.txt'):
            ssh_cli(SSHClient(srv, port, user, password), cmd)
