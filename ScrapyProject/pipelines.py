# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter.adapter import ItemAdapter
import json


class ScrapyProjectPipeline:
    pass
    # def process_item(self, item, spider):
    #     output_file = 'output.json'

    #     # Flatten the rarity field
    #     item['rarity'] = item['rarity'].strip() if 'rarity' in item else None

    #     with open(output_file, 'a', encoding='utf-8') as f:
    #         line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    #         f.write(line)

    #     return item
