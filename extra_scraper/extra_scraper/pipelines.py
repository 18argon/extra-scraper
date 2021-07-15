# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter
from extra_scraper.items import ReviewItem, ProductItem


class ExtraScraperPipeline:
    def process_item(self, item, spider):
        return item

class JsonLinesExportPipeline:

    def open_spider(self, spider):
        datestring = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

        self.exporters = {
            'products': {},
            'reviews': {},
        }

        for type in self.exporters:
            self.exporters[type]['file'] = open(f'{type}-{datestring}.jl', 'wb')
            self.exporters[type]['exporter'] = JsonLinesItemExporter(self.exporters[type]['file'])
            self.exporters[type]['exporter'].start_exporting()

    def close_spider(self, spider):
        for type in self.exporters:
            self.exporters[type]['exporter'].finish_exporting()
            self.exporters[type]['file'].close()

    def _get_exporter(self, item):
        if isinstance(item,ReviewItem):
            return self.exporters['reviews']['exporter']
        elif isinstance(item, ProductItem):
            return self.exporters['products']['exporter']
        return None

    def process_item(self, item, spider):
        self._get_exporter(item).export_item(item)