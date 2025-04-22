"""
Run the spider, get new job offers and send an email every 24h
"""
import sched
import datetime
import os
from time import sleep
from src.pipelines import new_offers, adapt_datetime, convert_datetime
import smtplib
import sqlite3
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.spiders.pracuj import PracujSpider

sqlite3.register_converter('datetime', convert_datetime)
sqlite3.register_adapter(datetime.datetime, adapt_datetime)

SMTP_SERVER = "smtp.gmail.com"
SENDER = os.getenv('senderemail')
RECEIVER = os.getenv('receiveremail')
PASSWORD = os.getenv("emailerpassword")




def my_sleep(time: datetime.timedelta) -> None:
    """ delayfunc for sched.scheduler that accepts datetime"""
    if time.total_seconds() <= 0:
        sleep(0)
    else:
        sleep(int(time.total_seconds()))

def send_mail(TO, MSG) -> None:
    with smtplib.SMTP(SMTP_SERVER) as smtp:
        smtp.starttls()
        smtp.login(SENDER, PASSWORD)
        smtp.sendmail(SENDER, TO, MSG)

def construct_mail(offers:list):
    pass


if __name__ == "__main__":
    con = sqlite3.connect("items.db", detect_types=sqlite3.PARSE_DECLTYPES) # doesnt seem to break stuff when db does not exist yet
    cur = con.cursor()
    a = cur.execute("DELETE FROM JobOffers WHERE JULIANDAY(date) - JULIANDAY() > 30") #delete offers that are older than 1 month and have not been updated
    con.commit()
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(PracujSpider)
    crawler.start()
    send_mail(RECEIVER, "hello")

    """  
    while True:
        scheduler = sched.scheduler(datetime.datetime.now, my_sleep)
        scheduler.enterabs()"""