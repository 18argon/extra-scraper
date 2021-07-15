# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    productId = scrapy.Field()
    skuId = scrapy.Field()
    filter_code = scrapy.Field
    title = scrapy.Field()
    url = scrapy.Field()
