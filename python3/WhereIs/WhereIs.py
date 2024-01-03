#!/bin/python3

import requests
import colorama
from ipaddress import ip_address
URL = "https://api.ipgeolocation.io/ipgeo"


# ADD YOUR KEY HERE
# ADD YOUR KEY HERE
# ADD YOUR KEY HERE
key = "" # <--- KEY HERE
# ADD YOUR KEY HERE
# ADD YOUR KEY HERE
# ADD YOUR KEY HERE


# just a habit not neccesary
if __name__ == "__main__" and key != "":
    from sys import argv
    # show help message
    if len(argv) > 1: address = argv[1]
    else:
        print(colorama.Fore.RED + "[!] missing IP address")
        print(colorama.Fore.YELLOW+"SYNTAX: python3 Whereis.py {ip1} [ipaddress2]...")
        quit()

    # loop on ip addresses
    for address in argv[1:]:
        try:
            # reading/validating user input
            ip_address(address)
            # request from API
            response = requests.get(f"{URL}?apiKey={key}&ip={address}").json()
            try:
                # shown output message
                message = colorama.Fore.GREEN + response['ip'] + ' is in ' + response["country_name"]+ ' using ' + response["isp"] + " services"
            except KeyError:
                message = f"{colorama.Fore.RED} [!] unexpected JSON format"
                print(f"raw response:\n{response}")
        # not valid IP addresses case
        except ValueError: message = f"{colorama.Fore.RED}{address} is not a valid IPv4 or IPv6 address"
        # present output
        print(message)
else:
    print(f"{colorama.Fore.Yellow}[!] APIkey is messing, add your API key in the script!")
    quit()
