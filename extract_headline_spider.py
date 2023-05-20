import scrapy
import pickle

class EkantipurSpider(scrapy.Spider):
    name = 'ekantipur'
    start_urls = ['https://ekantipur.com/news']

    def parse(self, response):
        extracted_data = []
        for teaser in response.css('div.teaser.offset'):
            text = teaser.css('h2 a::text').get()
            extracted_data.append(text)

        with open('output.pkl', 'wb') as file:
            pickle.dump(extracted_data, file)
