from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import json
import time

# Function to save data to SQLite database
def save_to_sqlite(data, db_filename="sequoia_companies.db"):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # Create a table for the companies if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT NOT NULL,
            company_url TEXT NOT NULL
        )
    """)

    # Insert data into the table
    for entry in data:
        cursor.execute("""
            INSERT INTO companies (company_name, company_url) VALUES (?, ?)
        """, (entry["company"], entry["url"]))

    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Data successfully saved to {db_filename}")


# Base URL for Sequoia Capital "Our Companies" page
base_url = "https://www.sequoiacap.com/companies/"

# Setup Selenium WebDriver
driver = webdriver.Chrome()

# Open the base URL
driver.get(base_url)

# Wait for the main page to load
time.sleep(5)

# Scroll through the page to load all dynamic content
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for new content to load

    # Check if scrolling has reached the bottom
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract all company links
companies = []
try:
    # Locate all links pointing to company pages
    WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a"))
    )
    company_links = driver.find_elements(By.CSS_SELECTOR, "a")

    # Filter links that match the company URL pattern
    for link in company_links:
        try:
            # Extract the URL
            company_url = link.get_attribute("href")

            # Filter for valid company URLs under the base URL
            if company_url and company_url.startswith(base_url):
                # Extract company name from the URL suffix
                company_name = company_url.replace(base_url, "").strip("/").replace("-", " ").title()

                # Avoid duplicates
                if not any(c['url'] == company_url for c in companies):
                    companies.append({"company": company_name, "url": company_url})

        except Exception as e:
            print(f"Error processing link: {e}")

except Exception as e:
    print(f"Error locating company links: {e}")

# Close the browser
driver.quit()

# Save data to a JSON file
output_filename = "sequoia_companies.json"
with open(output_filename, "w", encoding="utf-8") as json_file:
    json.dump(companies, json_file, ensure_ascii=False, indent=4)

# Print the content of the JSON file
print("\nExtracted Companies:")
print(json.dumps(companies, indent=4, ensure_ascii=False))

# Save data to SQLite database
save_to_sqlite(companies)
