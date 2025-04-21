# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import datetime

def adapt_datetime(val:datetime.datetime):
    return val.isoformat()
def convert_datetime(val):
    return datetime.datetime.fromisoformat(val.decode())

sqlite3.register_adapter(datetime.datetime, adapt_datetime)
sqlite3.register_converter("datetime",convert_datetime)

connection = sqlite3.connect("items.db", detect_types=sqlite3.PARSE_DECLTYPES)
cur = connection.cursor()

new_offers = []

db_ready = bool(cur.execute("SELECT name FROM sqlite_master WHERE name='JobOffers'").fetchone())
if not db_ready:
    cur.execute("CREATE TABLE JobOffers(title, company, location, date datetime)")
    #cur.execute("CREATE TABLE JobOffers(title, company, location, link, date datetime)")


class SrcPipeline:
    def process_item(self, item, spider):
        offer = cur.execute("SELECT * FROM JobOffers WHERE title=? AND company=? AND location=?", (item['title'], item['company'], item['location']))
        if offer.fetchone():
            cur.execute("UPDATE JobOffers SET date=? WHERE title=? AND company=? AND location=?", (item['date'], item['title'], item['company'], item['location']))
            connection.commit()
            return
        else:
            cur.execute("INSERT INTO JobOffers (title, company, location, date) VALUES (?, ?, ?, ?)", (item['title'], item['company'], item['location'], item['date']))
            #cur.execute("INSERT INTO JobOffers (title, company, location, date, link) VALUES (?, ?, ?, ?, ?)",(item['title'], item['company'], item['location'], item['date'], item['link']))
            connection.commit()
            new_offers.append(item)
            return item
