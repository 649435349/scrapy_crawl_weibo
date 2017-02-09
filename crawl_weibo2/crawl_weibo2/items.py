# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlWeibo2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_name = scrapy.Field()
    post_user = scrapy.Field()
    post_month = scrapy.Field()
    repost_cnt = scrapy.Field()
    thumbs_up_cnt = scrapy.Field()
    reply_cnt = scrapy.Field()
    t_when = scrapy.Field()
    content = scrapy.Field()
