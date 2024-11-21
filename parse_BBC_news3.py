import requests
from bs4 import BeautifulSoup
import json

# URL of the BBC Sport website
url = 'https://www.bbc.com/sport'

# Send GET request to fetch the page content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first 5 articles using the class 'ssrcss-zmz0hi-PromoLink' for links
    articles = soup.find_all('a', class_='ssrcss-zmz0hi-PromoLink', limit=5)

    # List to store the data for JSON output
    news_data = []

    for article in articles:
        # Get the article link (check if it has href attribute and form the full URL)
        link = article.get('href')
        if link:
            if not link.startswith('http'):
                link = 'https://www.bbc.com' + link  # Complete relative URL if necessary

            # Find the related topics (they are typically found in sibling elements or within the article's context)
            topics = []
            # Try to find any topic-related <span> or other elements
            topic_elements = article.find_all('span', class_='ssrcss-1mhwnz8-Promo')
            for topic in topic_elements:
                topics.append(topic.get_text().strip())

            # Store the collected data in the required JSON format
            news_data.append({
                'Link': link,
                'Topics': topics
            })

    # File name
    filename = "BBC_news_data.json"

    # Save the data to a JSON file
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(news_data, json_file, ensure_ascii=False, indent=4)

    # Print the content of the JSON file to the screen
    with open(filename, 'r', encoding='utf-8') as json_file:
        print(json_file.read())

else:
    print("Failed to retrieve the page. Status code:", response.status_code)
