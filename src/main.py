"""
Run the spider, get new job offers and send an email every 24h
"""
import sched
import datetime
from time import sleep
from src.pipelines import new_offers
import smtplib
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.spiders.pracuj import PracujSpider

def my_sleep(time: datetime.timedelta) -> None:
    """ delayfunc for sched.scheduler that accepts datetime"""
    if time.total_seconds() <= 0:
        sleep(0)
    else:
        sleep(int(time.total_seconds()))

def send_mail(text)-> None:
    print("-"*50)
    print("job offers to be sent: ", text)
    print("-" * 50)
    return None



if __name__ == "__main__":
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(PracujSpider)
    crawler.start()
    send_mail(new_offers)
    """    
    while True:
        scheduler = sched.scheduler(datetime.datetime.now, my_sleep)
        scheduler.enterabs()"""