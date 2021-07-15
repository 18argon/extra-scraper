# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import datetime
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter

class ExtraScraperPipeline:
    def process_item(self, item, spider):
        return item

class JsonLinesExportPipeline:

    def open_spider(self, spider):
        datestring = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')

        self.file = open(f'{spider.name}-{datestring}.jl', 'wb')
        self.exporter = JsonLinesItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)