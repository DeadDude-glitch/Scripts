

# Try to replicate the command curl https://api.macvendors.com/24:f5:a2:17:d3:35#
# The web application is free unless u wish to do more than 1 request per second and over 1000 request per day


# Module Imports

from requests import get
from time import sleep
from random import uniform
from multiprocessing import Process, Queue, Lock


# Do not have colorama? no problem!

try: 
    from colorama import Fore, Style
    red = Fore.RED
    green = Fore.GREEN
    yellow = Fore.YELLOW
    reset = Style.RESET_ALL
    dim = Style.DIM

except ModuleNotFoundError:
    red = ''
    green = ''
    yellow = ''
    reset = ''
    dim = ''


# function that takes the MAC address as a string and return raw API output

def _API_Call(addrs:str) -> str:
    
    # Constants Values Regarding API
    url = 'https://api.macvendors.com/'

    # Attempt to get the vendor of the MAC address
    # Minimal needed hardcoded response handling to expected output
    
    try: 
        Vendor = get(url + str(addrs)).text
        return Vendor
    
    # handling network errors
    except ConnectionError: return None
 

# return a human readable output of the MAC address vendor

def vendor(addrs:str, output:Queue, lock:Lock) -> str:
    
    # Constants Values Regarding API
    url = 'https://api.macvendors.com/'

    # Attempt to get the vendor of the MAC address
    # Minimal needed hardcoded response handling to expected output
    
    try:
        Vendor = _API_Call(str(addrs))
        if Vendor == None: raise ValueError
    
    # handling no value return error
    
    except ValueError:
        msg = "Connection failed for " + red + addrs + '\n' + reset
        return msg

    try: 

        # API failed

        if Vendor == '{"errors":{"detail":"Not Found"}}':
            msg = "Vendor of " + red + addrs + reset + " Not Found in API database"
        
        # You were to fast try again after some random time

        elif Vendor == '{"errors":{"detail":"Too Many Requests","message":"Please slow down your requests or upgrade your plan at https://macvendors.com"}}':
            sleep(uniform(0.2,0.6))
            msg = vendor(addrs, output, lock)

        # API worked

        else: msg = "Vendor of " + green + addrs + reset + ' is ' + green + Vendor + reset
    
    # Owning Your Code Error
    
    except: msg = red + "Script Error Occured for " + addrs + reset
    
    # Return whatever the output into the Multiproccessing Queue

    lock.acquire()
    output.put(msg)
    lock.release()

    return msg




# Customizable Driver Function

def main(window:int, MAC:list) -> list:
    
    # Required initialized values

    current = 0
    lock = Lock()
    queue = []
    output = Queue()

    # Till addresses are not over
    # Utilize the full window

    while current <= len(MAC)-1:
        
        
        for i in range(window):
            try:
                tmp = Process(target=vendor, args=(MAC[current],output,lock))
                tmp.start()
                queue.append(tmp)
            except IndexError: pass
            current += 1
            
        # Wait till you get more window
        
        sleep(1)
        
    # Display Output on console for CLI users
    
    value = []

    for thread in queue:
        thread.join()
        value.append(output.get(timeout=2))
        #print(value[len(MAC)-current])
        
    print(f"{yellow}Attempted to resolve {len(queue)} MAC addresses{reset}")
    return value
 


# CLI usage for testing

if __name__ == '__main__':
    
    # CLI Modules only

    from sys import argv
    
    if len(argv) <=1 or '-h' in argv or 'help' in argv:
        print(yellow + "[Syntax Error] Example: \n" + reset + "python mac_vendor.py " + green + "{MAC-address-1}[MAC-address-2] ..." + reset)
        exit()
    
    # execution call
    for msg in main(2, list(set(argv[1:]))): print(msg)
    
