import requests
import time
from urllib.parse import urlparse
import webbrowser

# List of URLs to check
urls = [
    "https://starfreebies.co.uk/get/cadbury-45/",
    "https://starfreebies.co.uk/get/cadbury-44/",
    "https://starfreebies.co.uk/get/cadbury-43/",
    "https://starfreebies.co.uk/get/cadbury-41-2/",
    "https://starfreebies.co.uk/get/cadbury-41/",
    "https://starfreebies.co.uk/get/cadbury-40/",
    "https://starfreebies.co.uk/get/cadbury-39/",
    "https://starfreebies.co.uk/get/cadbury-35-2/",
    "https://starfreebies.co.uk/get/cadbury-37/",
    "https://starfreebies.co.uk/get/cadbury-36/",
    "https://starfreebies.co.uk/get/cadbury-35/",
    "https://starfreebies.co.uk/get/cadbury-34/",
    "https://starfreebies.co.uk/get/cadbury-33/",
    "https://starfreebies.co.uk/get/cadbury-32/",
    "https://starfreebies.co.uk/get/cadbury-31/",
    "https://starfreebies.co.uk/get/cadbury-30/",
    "https://starfreebies.co.uk/get/cadbury-29/",
    "https://starfreebies.co.uk/get/cadbury-27-2/",
    "https://starfreebies.co.uk/get/cadbury-27/",
    "https://starfreebies.co.uk/get/cadbury-26/",
    "https://starfreebies.co.uk/get/cadbury-25/",
    "https://starfreebies.co.uk/get/cadbury-21/",
    "https://starfreebies.co.uk/get/cadbury-20/",
    "https://starfreebies.co.uk/get/cadbury-19/",
    "https://starfreebies.co.uk/get/cadbury-18/",
    "https://starfreebies.co.uk/get/cadbury-17/",
    "https://starfreebies.co.uk/get/cadbury-17-2/",
    "https://starfreebies.co.uk/get/cadbury-15/",
    "https://starfreebies.co.uk/get/cadbury-14/",
    "https://starfreebies.co.uk/get/cadbury-13/",
    "https://starfreebies.co.uk/get/cadbury-11-2/",
    "https://starfreebies.co.uk/get/cadbury-11/",
    "https://starfreebies.co.uk/get/cadbury-10/",
    "https://starfreebies.co.uk/get/cadbury-9/",
    "https://starfreebies.co.uk/get/cadbury-8/",
    "https://starfreebies.co.uk/get/cadbury-7/",
    "https://starfreebies.co.uk/get/cadbury-6/",
    "https://starfreebies.co.uk/get/cadbury-5/",
    "https://starfreebies.co.uk/get/cadbury-4/",
    "https://starfreebies.co.uk/get/cadbury-3/",
    "https://starfreebies.co.uk/get/cadbury-2/",
    "https://starfreebies.co.uk/get/cadbury-1/"
]

def check_redirect(url):
    try:
        # Send a HEAD request to avoid downloading the entire page
        response = requests.head(url, allow_redirects=True, timeout=10)
        final_url = response.url
        
        # Parse the final URL to get the path
        parsed_url = urlparse(final_url)
        
        # Check if the final URL path contains 'missed-out'
        if 'missed-out' in parsed_url.path:
            return False, final_url
        else:
            return True, final_url
    except requests.RequestException as e:
        return False, str(e)

while True:
    for url in urls:
        status, redirect_url = check_redirect(url)
        if status:
            print(f"{url} redirects to {redirect_url} (Not 'missed-out').")
            # Open the URL in browser if it doesn't redirect to 'missed-out'
            webbrowser.open(redirect_url)
        else:
            print(f"{url} either redirects to 'missed-out' or encountered an error: {redirect_url}")
    
    # Wait for one minute before the next check
    time.sleep(60)
