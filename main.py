import json
import datetime
import random
import string
import time
import os
import sys
import threading

try:
    import httpx
except ImportError:
    print("httpx package not found. Installing...")
    os.system("pip install httpx")
    import httpx

# Define script version and window title
script_version = '4.4.0'
window_title = f"WARP-PLUS-CLOUDFLARE (version {script_version})"

# Set window title based on OS
os.system(
    f'title {window_title}'
    if os.name == 'nt'
    else 'PS1="\[\e]0;' + window_title + '\a\]"; echo $PS1'
)

# Clear console screen based on OS
os.system('cls' if os.name == 'nt' else 'clear')

# Print information about the script (without your name and website)
print("[+] ABOUT SCRIPT:")
print("[-] With this script, you can obtain unlimited WARP+ referral data.")
print(f"[-] Version: {script_version}")
print("[♡] Made with ♡ by Navaneeth K M (nxvvvv)")
print("--------")

# Initialize user settings
referrer = ""
min_interval = 10  # Default minimum request interval (seconds)
max_interval = 60  # Default maximum request interval (seconds)
save_file = "warp.sav"
stop_flag = False

# Load referral data and saved client IDs from script data structures
referral_data = {
    "users": {},
    "total": {
        "total_referrals": 0
    }
}

# Function to generate a random string
def genString(stringLength):
    try:
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(stringLength))
    except Exception as error:
        print(error)

# Function to generate a random digit string
def digitString(stringLength):
    try:
        digit = string.digits
        return ''.join(random.choice(digit) for _ in range(stringLength))
    except Exception as error:
        print(error)

# Define the API URL
url = f'https://api.cloudflareclient.com/v0a{digitString(3)}/reg'

# Function to send a request to the API and handle the response
def run():
    global stop_flag
    try:
        install_id = genString(22)
        body = {
            "key": f"{genString(43)}=",
            "install_id": install_id,
            "fcm_token": f"{install_id}:APA91b{genString(134)}",
            "referrer": referrer,
            "warp_enabled": False,
            "tos": f"{datetime.datetime.now().isoformat()[:-3]}+02:00",
            "type": "Android",
            "locale": "es_ES",
        }
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Host': 'api.cloudflareclient.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.1'
        }

        with httpx.Client() as client:
            response = client.post(url, json=body, headers=headers)

        if response.status_code == 200:
            print(f"\n[-] WORK ON ID: {referrer}")
            print(f"[:)] Request completed successfully.")
            return True
        else:
            print("[:(] Error when connecting to server.")
            return False
    except Exception as error:
        print("")
        print(error)
        return False

# Function to start the script
def start_script():
    global stop_flag
    g = 0
    b = 0
    stop_flag = False

    # Start the thread to check for the 's' key press
    stop_thread = threading.Thread(target=check_stop_key)
    stop_thread.daemon = True
    stop_thread.start()

    while not stop_flag:
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.write("\r[+] Sending request...")
        sys.stdout.flush()
        result = run()
        if result:
            g += 1
            if referrer in referral_data["users"]:
                referral_data["users"][referrer][1] += 1  # Increment successful referrals
            else:
                referral_data["users"][referrer] = [referrer, 1]  # Initialize successful referrals to 1
            referral_data["total"]["total_referrals"] += 1
            update_log_file()
            print(f"[:)] {g} GB has been successfully added to your account.")
            print(f"[#] Total: {g} Good {b} Bad")
            for i in range(max_interval, 0, -1):
                sys.stdout.write(f"\r[*] After {i} seconds, a new request will be sent.")
                sys.stdout.flush()
                time.sleep(1)  # Wait for the maximum request interval
        else:
            b += 1
            print("\n[:(] Error when connecting to server.")
            print(f"[#] Total: {g} Good {b} Bad")
            for i in range(min_interval, 0, -1):
                sys.stdout.write(f"\r[*] Retrying in {i}s...")
                sys.stdout.flush()
                time.sleep(1)  # Wait for the minimum request interval

# Function to update the log file with referral data
def update_log_file():
    global referral_data
    with open(save_file, "w") as log_file:
        json.dump(referral_data, log_file, indent=2)

# Function to check for the 's' key press to stop the script
def check_stop_key():
    global stop_flag
    while True:
        if input("Press 's' and Enter to stop the script: ").strip().lower() == 's':
            stop_flag = True
            print("\n[!] Stopping the script...")
            break

# Main script loop
while True:
    print("\n[+] MENU:")
    print("1. Start Script")
    print("2. Set Minimum Request Interval")
    print("3. Set Maximum Request Interval")
    print("4. Set Referrer (User ID)")
    print("5. Display Referral Data")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        if not referrer:
            referrer = input("Enter the Referrer (User ID): ")
        start_script()
    elif choice == '2':
        min_interval = int(input("Enter Minimum Request Interval (seconds): "))
    elif choice == '3':
        max_interval = int(input("Enter Maximum Request Interval (seconds): "))
    elif choice == '4':
        referrer = input("Enter the Referrer (User ID): ")
    elif choice == '5':
        print("Referral Data:")
        print(json.dumps(referral_data, indent=2))
    elif choice == '6':
        print("[+] Exiting the script.")
        break
    else:
        print("[!] Invalid choice. Please select a valid option.")
