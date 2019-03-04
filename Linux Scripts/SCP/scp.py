"""
    Before use script you should install the next librory:
    pip install scp
    pip install paramiko
    pip install pyyaml
    pip install cryptography==2.4.2 or later version
    or you can use requirements file, for example
    pip install -r requirements.txt

"""

import paramiko
from scp import SCPClient
import yaml

""" 
    Parameters of authentications
    which are located in mp.yaml file 
"""

scp = yaml.load(open('scp.yaml'))
port = scp['port']
user = scp['user']
password = scp['password']

from_path = '/YourFolder/scp.file'
to_path = '/to/path'

def ssh_cli(server, port, user, password):
    """ This function creating to connection """
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

if __name__ == '__main__':
    for ip in open('ip_list.csv'):
        ssh = ssh_cli(ip, port, user, password)
        scp = SCPClient(ssh.get_transport())
        scp.put(from_path, remote_path=to_path)
        print('File {} copied on {}'.format(from_path, to_path))
        scp.close()
