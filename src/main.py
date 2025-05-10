"""
Run the spider, get new job offers and send an email every 24h
"""
import sched
import datetime
import os
from time import sleep
from src.pipelines import new_offers, adapt_datetime, convert_datetime
import smtplib
from email.mime.text import MIMEText
import sqlite3
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from twisted.internet import asyncioreactor
asyncioreactor.install()
from twisted.internet import task, reactor
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

def send_mail(MSG) -> None:
    with smtplib.SMTP(SMTP_SERVER) as smtp:
        smtp.starttls()
        smtp.login(SENDER, PASSWORD)
        smtp.send_message(MSG)
        print(f"Email sent at {datetime.datetime.now()}")

def construct_mail(SENDER, RECEIVER, offers):
    offers_string = ""
    for i in offers:
        offers_string += (f"      {i['title']} - {i['company']} - {i['location']} \n \n")

    text = f"""
    Hello!

    These are the offers published on pracuj.pl in the last 24h:

{offers_string}

    Hope they're to your liking. See you tommorow!
                """
    msg = MIMEText(text)
    msg['To'] = RECEIVER
    msg['From'] = SENDER
    msg['Subject'] = "Your daily job offers from Pracuj.pl!"
    return msg

if __name__ == "__main__":
    crawler = CrawlerRunner(get_project_settings())

    def aaaa():
        con = sqlite3.connect("items.db", detect_types=sqlite3.PARSE_DECLTYPES) # doesnt seem to break stuff when db does not exist yet
        cur = con.cursor()
        cur.execute("DELETE FROM JobOffers WHERE JULIANDAY(date) - JULIANDAY() > 30") #delete offers that are older than 1 month and have not been updated
        con.commit()
        con.close()

        crawler.crawl(PracujSpider)

        mail = construct_mail(SENDER, RECEIVER, new_offers)
        send_mail(mail)


    # b = task.LoopingCall(aaaa)
    # b.start(120)
    # reactor.run()
    aaaa()