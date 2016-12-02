# python
import os.path
import dns.resolver
import dns.exception
from time import sleep
import argparse
from colorama import init, Fore

init()

dictfile = 'list.txt'
wait = 0.06

resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4', '208.67.222.222', '208.67.220.220']

parser = argparse.ArgumentParser(description='\ndnsbrute - DNS subdomain bruteforce scanner by martijn0x76\n')
parser.add_argument('--domain', '-d', help='domain to test', required=True)
parser.add_argument('--out', '-o', help='output to textfile', required=False)

args = parser.parse_args()

domain = args.domain

if os.path.exists(dictfile):
    f = open(dictfile, "r")
    for line in iter(f):
        l = line.strip('\n')
        try:
            answer = resolver.query(l + "." + domain)
            ip = ''
            for a in answer:
                ip = ip + str(a) + ' '
            print Fore.GREEN + l + "." + domain + "\t" + ip
            if args.out is not None:
                with open(args.out, "a") as outfile:
                    outfile.write(l + "." + domain + '\n')
        except dns.exception.DNSException as e:
            if isinstance(e, dns.resolver.NXDOMAIN):
                continue
            elif isinstance(e, dns.resolver.Timeout):
                print Fore.RED + 'Time-out'
            else:
                print Fore.RED + 'Unhandled exception'
        finally:
            sleep(wait)
    f.close()
