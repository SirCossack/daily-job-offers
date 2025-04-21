import datetime

import scrapy
from bs4 import BeautifulSoup
if __name__ == "spiders.pracuj":
    from src.src.items import JobOffer
else:
    from ..items import JobOffer


class PracujSpider(scrapy.Spider):
    name = "pracuj"
    allowed_domains = ["it.pracuj.pl", "pracuj.pl"]
    start_urls = ["https://it.pracuj.pl/praca?et=17&itth=37"]


    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find("div", attrs={"data-test": "section-offers"})
        count = 0
        for i in jobs.children:
            count +=1
            title = i.find("h2", attrs={"data-test": "offer-title"}).text
            company = i.find("h3", attrs={"data-test": "text-company-name"}).text
            location = i.find("h4", attrs={"data-test": "text-region"}).text
            #link = i.find_all("a", attrs={"data-test": "link-offer"})[0]['href']
            #yield JobOffer(title=title, company=company, location=location, date=datetime.datetime.now(), link=link)
            yield JobOffer(title=title, company=company, location=location, date=datetime.datetime.now())