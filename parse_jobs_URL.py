import requests
import re
import json
import sqlite3
from bs4 import BeautifulSoup

# URL of the website
url = 'https://www.lejobadequat.com/emplois'

# Send GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all job elements (e.g., <a> tags that contain job title and links)
    job_elements = soup.find_all('a', href=True)

    # List to store job titles and URLs
    job_data = []

    # Regular expression to find job titles (adjust based on actual structure)
    for job in job_elements:
        title = job.get_text().strip()  # Get the job title text
        link = job['href']  # Get the URL (href attribute)
        
        # Use regex to filter out jobs that may have "H/F" or other criteria
        match = re.search(r'(.+)', title)  # Modify as necessary for specific title pattern
        
        if match:
            job_data.append({"title": match.group(1), "url": link})

    # 1. Save the result in JSON format
    with open('job_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(job_data, json_file, ensure_ascii=False, indent=4)

    # 2. Save the result in an SQLite database
    # Connect to SQLite database (or create one if it doesn't exist)
    conn = sqlite3.connect('job_data.db')
    cursor = conn.cursor()

    # Create the jobs table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')

    # Insert data into the jobs table
    for job in job_data:
        cursor.execute('''
            INSERT INTO jobs (title, url)
            VALUES (?, ?)
        ''', (job['title'], job['url']))

    # Commit and close the database connection
    conn.commit()
    conn.close()

    print("Data has been successfully saved in JSON and SQLite formats.")
else:
    print("Failed to retrieve the page. Status code:", response.status_code)