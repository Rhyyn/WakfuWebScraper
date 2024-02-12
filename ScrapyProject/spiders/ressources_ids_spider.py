import scrapy
import os
import json
import re

# does not include page 1 for some reason


class RessourcesIdsSpider(scrapy.Spider):
    name = "ressources_ids"
    base_url = "https://www.wakfu.com/fr/mmorpg/encyclopedie/ressources?page={}"
    items = []

    def start_requests(self):
        # Generate start URLs for 80 pages
        start_urls = [self.base_url.format(page) for page in range(1, 81)]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("Parsing page: ", response.url)
        # Extracting href links, corresponding names, levels, and rarities
        for row in response.css("table tbody tr"):
            link = row.css("td:nth-child(2) span.ak-linker a")
            name = link.css("::text").get()
            href = link.attrib["href"]
            resource_id = href.split("/")[-1].split("-")[0]
            self.items.append(resource_id)
        yield {"page": response.url, "resources": self.items}

    def closed(self, reason):
        file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "ScrapedData",
            "ScrapedFiles",
            "ScrapedRessources",
            "ressources_ids.json",
        )
        # Save the scraped data
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.items, file, ensure_ascii=False, indent=2)
