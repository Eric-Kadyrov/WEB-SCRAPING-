import requests
from bs4 import BeautifulSoup
import json

# Step 1: Fetch the HTML content of the webpage
url = "https://www.bbc.com/sport"
response = requests.get(url)

# Ensure the response is valid
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Step 2: Extract the first 5 news articles
    news_data = []
    articles = soup.find_all("a", class_="sp-o-link-split__anchor", limit=5)  # Corrected class name

    for article in articles:
        link = "https://www.bbc.com" + article.get('href')  # Construct full link
        topics = []

        # Attempt to find related topics
        parent_div = article.find_parent("div", class_="sp-c-promo")  # Locate parent div for context
        if parent_div:
            topic_tags = parent_div.find_all("span", class_="sp-c-promo__tag")
            topics = [tag.get_text(strip=True) for tag in topic_tags]

        # Add data to the list
        news_data.append({
            "Link": link,
            "Topics": topics if topics else ["Uncategorized"]  # Default to Uncategorized if no topics found
        })
    
    # Step 3: Save the data in JSON format
    with open("bbc_sport_news.json", "w") as file:
        json.dump(news_data, file, indent=4)
    
    print("News data saved to bbc_sport_news.json")
else:
    print("Failed to retrieve the webpage.")