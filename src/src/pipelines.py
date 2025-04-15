# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

connection = sqlite3.connect("items.db")
cur = connection.cursor()

db_ready = bool(cur.execute("SELECT name FROM sqlite_master WHERE name='JobOffers'").fetchone())
if not db_ready:
    cur.execute("CREATE TABLE JobOffers(title, company, location)")


class SrcPipeline:
    def process_item(self, item, spider):
        offer = cur.execute(f"SELECT * FROM JobOffers WHERE title=? AND company=? AND location=?", (item['title'], item['company'], item['location']))
        if offer.fetchone():
            return
        else:
            cur.execute("INSERT INTO JobOffers (title, company, location) VALUES (?, ?, ?)", (item['title'], item['company'], item['location']))
            connection.commit()
            return item

class SendMail:
    def process_item(self, item, spider):
        if not item:
            return
        else:
            print(f"Item to send: {item}")
            return item