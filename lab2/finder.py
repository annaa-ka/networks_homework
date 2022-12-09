import argparse
import re
import subprocess
import ipaddress

IP_HEADER_SIZE = 20
ICMP_HEADER_SIZE = 8

def check_host_validity(host):
    reg_exp = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    if reg_exp.match(host):
        return True
    try:
        ipaddress.ip_address(host)
        return True
    except:
        return False


def check_if_icmp_enabled():

    process = subprocess.run(
        ["cat", "/proc/sys/net/ipv4/icmp_echo_ignore_all"],
        capture_output = True,
        text = True
    )

    if process.stdout == 1:
        print("ICMP is disabled.")
        if process.stdout != "":
            print(process.stdout)
        else:
            print(process.stderr)
        exit(1)
        
def ping_host(host, packet_size):
    process = subprocess.run(
        ["ping", host, "-M", "do", "-s", packet_size, "-c", "2"],
        capture_output = True,
        text = True
    )
    return process

    
def find_mtu(host):
    l, r = 0, 9001 - IP_HEADER_SIZE - ICMP_HEADER_SIZE
    while l + 1 < r:
        mid = (l + r) // 2
        process = ping_host(host, str(mid))
        if process.returncode == 0:
            l = mid
        elif process.returncode == 1:
            r = mid
        else:
            print(process.stderr)
            exit(1)
    return l
        
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host')
    
    args = parser.parse_args()
    host = args.host
    host_valid = check_host_validity(host)
    if not host_valid:
        print("Host ", host, " is not valid.")
        exit(1)
        
    check_if_icmp_enabled()
    
    mtu = find_mtu(host)
    print("MTU is equal to ", mtu + IP_HEADER_SIZE + ICMP_HEADER_SIZE)

if __name__ == '__main__':
    main()