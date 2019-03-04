import re
from collections import Counter
import csv
import subprocess
import os

def reader():
    locations = input('Specify path: ')
    file = input('Filename: ')
    regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    path = os.path.join(os.getcwd(), os.path.normpath(locations))
    with open(os.path.join(path, file)) as f:
        log = f.read()
        ips_list = re.findall(regexp, log)
        print(ips_list)
    return ips_list


def ufw_rules(ips_list):
    trusted_ip = []
    user_input = input('Please input trusted IP: ')
    trusted_ip.append(user_input.split())
    safe_ips = trusted_ip[0]
    print('You added: ', safe_ips)

    for ufw in ips_list:
        if ufw not in safe_ips: # Указать доверенные IP адреса
            subprocess.call(["ufw", "deny", "from", ufw])
    return ips_list


def count(ips_list):
    return Counter(ips_list)

def write_csv(count):
    with open('output.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)

        header = ['IP', 'Frequency']
        writer.writerow(header)

        for item in count:
            writer.writerow((item, count[item]))

if __name__ == '__main__':
    write_csv(count(ufw_rules(reader())))
