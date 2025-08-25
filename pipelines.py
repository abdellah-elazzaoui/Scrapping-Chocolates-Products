# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ChocolatescrapperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        value = adapter.get("title")
        adapter["title"]=value[0]

        # Price ---> Float:
        value = adapter.get('price')[0]
        if "From" in value:
            value=value.replace("From ","")
        adapter["price"]=float(value[1:])

        #Correct URL:
        value = adapter.get("url")
        value = "https://www.chocolate.co.uk"+value
        adapter["url"] = value

        return item

class DuplicatePipeline:
    def __init__(self):
        self.names = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["title"] not in self.names:
            self.names.add(adapter["title"])
            return item    
"""


import mysql.connector

class SaveToMySqlPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "abdellah2004",
            database="chocolates"
        )
        self.cur = self.conn.cursor()
        self.cur.execute("
        CREATE TABLE IF NOT EXISTS chocolate_products(
            id int not null auto_increment ,
            title text NOT NULL,
            price DECIMAL(6,4) not null,
            url varchar(255),
            primary key(id)
        )
        ")

    def process_item(self, item, spider):
        self.cur.execute("insert into chocolate_products (title,price,url) values(%s,%s,%s)",(item['title'],item['price'],item['url']))
        self.conn.commit()
        return item
    
    def close_connection(self,spider):
        self.cur.close()
        self.conn.close()

import psycopg2

class SaveToPGPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            user="root",
            password="root",
            dbname="chcolates"  
        )
        self.cur = self.conn.cursor()
        self.cur.execute("
        CREATE TABLE IF NOT EXISTS chocolate_products (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            price NUMERIC(10,2) NOT NULL,
            url VARCHAR(255)
        )
        ")
        self.conn.commit()

    def process_item(self, item, spider):
        self.cur.execute(
            "INSERT INTO chocolate_products (title, price, url) VALUES (%s, %s, %s)",
            (item['title'], item['price'], item['url'])
        )
        self.conn.commit()
        return item

    def close_spider(self, spider):  # correct Scrapy hook
        self.cur.close()
        self.conn.close()

        """