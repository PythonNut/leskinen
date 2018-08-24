import socket
from pathlib import Path

import sshconf
import netifaces as ni

# TODO: Make this generic
HOST_DIR = Path("~/Documents/etc/ssh/hosts").expanduser()

def get_hostname():
    return socket.gethostname().split('.')[0]

def get_host():
    iface = ni.gateways()['default'][ni.AF_INET][1]
    # TODO: What if we have multiple IP addresses?
    return ni.ifaddresses(iface)[ni.AF_INET][0]['addr']

def make_ssh_config(hostname, host):
    conf = sshconf.empty_ssh_config()
    conf.add(hostname, Hostname=host)
    return conf.config().strip()

def main():
    hostname = get_hostname()
    host = get_host()
    config = make_ssh_config(hostname, host)
    print(config)
    with open(HOST_DIR / f'{hostname}.conf', 'w') as f:
        f.write(config)

if __name__ == '__main__':
    main()
