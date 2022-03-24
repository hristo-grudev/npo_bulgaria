# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

from itemadapter import ItemAdapter


class NpoBulgariaPipeline:
    conn = sqlite3.connect('npo_bg.db')
    cursor = conn.cursor()

    def open_spider(self, spider):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS `npo_bg` (
                                                                            title varchar(100),
                                                                            kind text,
                                                                            domain text,
                                                                            url text
                                                                            )''')
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            title = item['title'].replace("'", '"').replace('`', '"')
        except:
            title = ''
        try:
            kind = item['kind'].replace("'", '"').replace('`', '"')
        except:
            kind = ''
        try:
            domain = item['domain']
        except:
            domain = ''
        try:
            url = item['url']
        except:
            url = ''

        self.cursor.execute(f"""select * from npo_bg where  url = '{url}'""")
        is_exist = self.cursor.fetchall()

        if len(is_exist) == 0:
            self.cursor.execute(
                f"""insert into `npo_bg` (`title`, `kind`, `domain`, `url`) values ('{title}', '{kind}', '{domain}', '{url}')""")
            self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
