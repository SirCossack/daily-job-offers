import scrapy
import pickle

class PracujSpider(scrapy.Spider):
    name = "pracuj"
    allowed_domains = ["it.pracuj.pl", "pracuj.pl"]
    start_urls = ["https://it.pracuj.pl/praca?et=17&itth=37"]

    def parse(self, response):
        with open('resp.pkcl', 'wb') as file:
            pickle.dump(response.text, file)
