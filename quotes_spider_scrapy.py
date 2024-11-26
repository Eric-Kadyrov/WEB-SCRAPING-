import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/page/1/']

    def parse(self, response):
        # Extract quote text and author from the current page
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span small::text').get(),
            }

        # Pagination: Check if there is a next page and follow the link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def closed(self, reason):
        # After the spider finishes, print the output file content
        output_filename = 'quotes_authors.json'

        # Open and read the output file
        try:
            with open(output_filename, 'r', encoding='utf-8') as json_file:
                content = json.load(json_file)
                # Print the content of the JSON file to the screen in a readable format
                print(json.dumps(content, indent=4, ensure_ascii=False))
        except Exception as e:
            print(f"Error reading file: {e}")