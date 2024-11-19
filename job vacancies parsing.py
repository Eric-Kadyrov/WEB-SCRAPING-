import requests
from bs4 import BeautifulSoup
import re

# URL of the website
url = 'https://www.lejobadequat.com/emplois'

# Send GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Example: Extract job titles (assuming the job titles are within <h2> tags)
    job_titles = soup.find_all('h2')

    # List to store clean job titles
    clean_job_titles = []

    # Iterate over each job title and clean it up using regex
    for job in job_titles:
        # Get the text and remove unnecessary spaces or characters
        title = job.get_text().strip()
        
        # Use regular expression to match job titles that contain "H/F"
        match = re.search(r'(.+H/F)', title)  # This will match titles ending with ' H/F'
        
        if match:
            # If a match is found, clean and add it to the list
            clean_job_titles.append(match.group(1))

    # Print the cleaned list of job titles
    print(clean_job_titles)
else:
    print("Failed to retrieve the page. Status code:", response.status_code)