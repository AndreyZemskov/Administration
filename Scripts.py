import re
from collections import Counter
import csv
import subprocess

def reader(filename):
    regexp = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    with open(filename) as f:
        log = f.read()
        ips_list = re.findall(regexp, log)
    return ips_list

def ufw_rules(ips_list):
    for ufw in ips_list:
        if ufw != '192.168.0.1':
            subprocess.call(["ufw", "deny", "from", ufw])
    return ufw

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
    write_csv(count(reader('access.log')))
    ufw_rules(reader('access.log'))