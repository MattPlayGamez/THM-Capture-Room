# Capture room Tryhackme.com login bypass

# THM Capture Cracker

This Python script, named `THM_CAPTURE_CRACKER.py`, is designed to crack the Capture rooms's credentials that has a math captcha.

## Dependencies

The script uses the following Python libraries:
- `requests`
- `BeautifulSoup` from `bs4`
- `re`
- `threading`
- `argparse`
- `time`
- `math`
- `warnings`

## Usage

The script is run from the command line with the following syntax:

```bash
python3 THM_CAPTURE_CRACKER.py http://{THM_IP}/login -ul usernames.txt -pl passwords.txt -iuq "does not exist" -ipq "Invalid" -v

Arguments
The script takes the following arguments:

url: The full URL for the requests.
-ul or --username-list: The location of the usernames list.
-pl or --password-list: The location of the passwords list.
-v or --verbose: Enable verbose mode (optional).
-iuq or --invalid-username-query: How the program should know when a username is invalid.
-ipq or --invalid-password-query: How the program should know when a password is invalid.
```
### How It Works
The script works by attempting to solve the captcha for each (POST) request and then brute forcing the username and password fields on the website. If it finds a valid username and password, it writes the successful login page to successfull_login.html and prints the cracked password, the time it took to crack the password.
```

### Note: Before using, force the captcha, by putting in the wrong combination multiple times
