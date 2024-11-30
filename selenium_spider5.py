from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Setup Selenium WebDriver
driver = webdriver.Chrome()

# Function to extract jobs from the current page
def extract_jobs():
    jobs = []
    try:
        # Wait for job elements to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.job-result"))
        )

        # Find job elements
        job_elements = driver.find_elements(By.CSS_SELECTOR, "li.job-result")

        for job_element in job_elements:
            try:
                # Extract job title
                title_element = job_element.find_element(By.CSS_SELECTOR, "h3.job-title")
                title = title_element.text.strip()

                # Extract job URL
                link_element = job_element.find_element(By.CSS_SELECTOR, "a.job-link")
                url = link_element.get_attribute("href")

                # Append to jobs list
                jobs.append({"title": title, "url": url})
            except Exception as e:
                print(f"Error extracting job: {e}")

    except Exception as e:
        print(f"Error locating job elements: {e}")

    return jobs

# Open the website
driver.get("https://jobs.marksandspencer.com/job-search")
time.sleep(3)  # Wait for the page to load

# Debugging: Print page source to check structure
# Uncomment the following line to inspect the HTML structure
# print(driver.page_source)

# Scrape first two pages
all_jobs = []
for page in range(2):  # First two pages
    print(f"Scraping page {page + 1}...")
    jobs = extract_jobs()
    all_jobs.extend(jobs)

    # Try to navigate to the next page
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.pagination-next"))
        )
        ActionChains(driver).move_to_element(next_button).click(next_button).perform()
        time.sleep(3)  # Wait for the next page to load
    except Exception as e:
        print(f"No more pages or next button not found: {e}")
        break

# Close the browser
driver.quit()

# Save to JSON file
output_filename = "jobs_descriptions.json"
with open(output_filename, "w", encoding="utf-8") as json_file:
    json.dump(all_jobs, json_file, ensure_ascii=False, indent=4)

# Print the content of the saved JSON file
print("\nScraped Job Listings:")
with open(output_filename, "r", encoding="utf-8") as json_file:
    content = json.load(json_file)
    print(json.dumps(content, indent=4, ensure_ascii=False))