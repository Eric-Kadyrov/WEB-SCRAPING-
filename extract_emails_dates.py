import re
import csv

# Open and read the text file
with open(r'C:\Users\User\Downloads\text.txt', 'r') as file:
    text_data = file.read()

# Regular expression for matching dates (example formats: yyyy-mm-dd, dd/mm/yyyy)
date_pattern = r'\b(?:\d{4}[-/]\d{2}[-/]\d{2}|\d{2}[-/]\d{2}[-/]\d{4})\b'

# Regular expression for matching email addresses
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Find all dates and emails in the text data
dates = re.findall(date_pattern, text_data)
emails = re.findall(email_pattern, text_data)

# Prepare data to be saved in CSV format
data = list(zip(dates, emails))

# Write the extracted data to a CSV file
with open(r'C:\Users\User\Downloads\Data.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header
    csv_writer.writerow(['Date', 'Email'])
    # Write rows of parsed data
    csv_writer.writerows(data)

print("Data has been successfully parsed and saved to Data.csv")