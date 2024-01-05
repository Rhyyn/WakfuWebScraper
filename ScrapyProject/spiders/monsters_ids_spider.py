import scrapy
import json
import os

class MonstersIdsSpider(scrapy.Spider):
    """
    -INFO-
    Spider to retrieve all the IDs of the monster, needed to run the monsters_data_spider.
    -------
    -USAGE-
    python -m cli crawl monsters_ids
    -------
    -OUTPUT-
    monsters_IDs.json
    --------
    """
    name = "monsters_ids"
    allowed_domains = ["wakfu.com"]
    start_url = 'https://www.wakfu.com/fr/mmorpg/encyclopedie/monstres?page={}'
    
    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.items = []

    def start_requests(self):
        # Start from page 1
        yield scrapy.Request(url=self.start_url.format(1), callback=self.parse)


    def parse(self, response):
        # Extract href from the second td in each tr
        for tr in response.css('tbody tr'):
            href = tr.css('td:nth-child(2) span a::attr(href)').get()
            # Extract the monster ID from the URL
            monster_id = int(href.rsplit('/', 1)[-1].split('-', 1)[0])
            self.logger.info(monster_id)
            self.items.append(monster_id)

        # Calculate the next page number
        current_page = int(response.url.split('=')[-1])
        next_page = current_page + 1

        # Follow the link to the next page if not exceeding the total number of pages (34)
        if next_page <= 35:
            yield response.follow(self.start_url.format(next_page), callback=self.parse)


    def closed(self, reason):
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'Output', 'monsters_IDs.json')
        print(file_path)
        # save the scraped data
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.items, file, ensure_ascii=False, indent=2)  # type: ignore