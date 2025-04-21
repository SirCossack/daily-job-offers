"""
Run the spider, get new job offers and send an email every 24h
"""
import sched
import datetime
from time import sleep
from src.pipelines import new_offers, adapt_datetime, convert_datetime
import smtplib
import sqlite3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.spiders.pracuj import PracujSpider

sqlite3.register_converter('datetime', convert_datetime)
sqlite3.register_adapter(datetime.datetime, adapt_datetime)

def my_sleep(time: datetime.timedelta) -> None:
    """ delayfunc for sched.scheduler that accepts datetime"""
    if time.total_seconds() <= 0:
        sleep(0)
    else:
        sleep(int(time.total_seconds()))

def send_mail(offers:list) -> None:
    print("-"*50)
    counter = 0
    for i in offers:
        print("job offers to be sent: ", i)
        counter +=1
    print(f"overall {counter} offers")
    print("-" * 50)
    return None



if __name__ == "__main__":
    con = sqlite3.connect("items.db", detect_types=sqlite3.PARSE_DECLTYPES) # doesnt seem to break stuff when db does not exist yet
    cur = con.cursor()
    a = cur.execute("DELETE FROM JobOffers WHERE JULIANDAY(date) - JULIANDAY() > 30") #delete offers that are older than 1 month and have not been updated
    con.commit()

    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(PracujSpider)
    crawler.start()
    send_mail(new_offers)
    """  
    while True:
        scheduler = sched.scheduler(datetime.datetime.now, my_sleep)
        scheduler.enterabs()"""