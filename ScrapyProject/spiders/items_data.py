from curses import panel
import scrapy
import re
import json
import math
import os
from ScrapyProject.middlewares import RotateUserAgentMiddleware


class ItemDataSpider(scrapy.Spider):
    """
    -INFO-
    Used to retrieve the missing droprates for each possible items
    -------
    -USAGE-
    python -m cli crawl items_data
    -------
    -OUTPUT-
    Inside the ScrappedData Folder
    --------
    """
    name = 'items_data'  
    start_urls = []
    results = []
    def get_starting_url(self, category_id:int, url_mapping):
        if not category_id:
            raise ValueError("Empty category_id")
        
        # param gets converted to str for some reason
        # need to convert it back to int | :)
        category_id = int(category_id)
        base_url = 'https://www.wakfu.com/fr/mmorpg/encyclopedie/'
        category_url = url_mapping.get(category_id, 'Unknown Category')

        return f'{base_url}{category_url}'


    def get_category_name(self, category_id):
        item_type_mapping = {
            120: 'amulette', 103: 'anneau', 119: 'bottes', 132: 'cape', 134: 'casque', 133: 'ceinture', 138: 'epaulettes', 136: 'plastron',
            254: 'arme1main', 108: 'arme1main', 110: 'arme1main', 115: 'arme1main', 113: 'arme1main', 223: 'arme2main', 114: 'arme2main', 101: 'arme2main', 111: 'arme2main', 253: 'arme2main', 117: 'arme2main', 112: 'secondemain', 189: 'secondemain',
            646: 'emblemes', 480: 'torches', 537: 'outils',
            812: 'sublimation',
            611: 'montures',
            582: 'familiers',
        }
        category_name = item_type_mapping.get(category_id)
        
        if category_name is None:
            raise ValueError(f"Invalid category ID: {category_id}")

        return category_name

    
    def get_id_mappings(self):
        url_mapping = {
            120: 'armures', 103: 'armures', 119: 'armures', 132: 'armures', 134: 'armures', 133: 'armures', 138: 'armures', 136: 'armures',
            254: 'armes', 108: 'armes', 110: 'armes', 115: 'armes', 113: 'armes', 223: 'armes', 114: 'armes', 101: 'armes', 111: 'armes', 253: 'armes', 117: 'armes', 112: 'armes', 189: 'armes',
            646: 'accessoires', 480: 'accessoires',537: 'accessoires',
            812: 'ressources',
            611: 'montures',
            582: 'familiers',
        }
        return url_mapping

    def __init__(self, category_id:int, *args, **kwargs):
        # param gets converted to str for some reason
        # need to convert it back to int | :)
        self.category_id = int(category_id) 
        url_mapping = self.get_id_mappings()
        self.start_url = self.get_starting_url(self.category_id, url_mapping)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        items_json_path = os.path.join(parent_dir, 'items.json')
        with open(items_json_path, 'r', encoding='utf-8') as file:
            items_data = json.load(file)

        filtered_ids = [item['definition']['item']['id'] 
                        for item in items_data if item.get('definition', {})
                                                        .get('item', {})
                                                        .get('baseParameters', {})
                                                        .get('itemTypeId') == int(self.category_id)] #type: ignore

        self.logger.info("Filtered Items: %s", filtered_ids)
        scrap_per_min = 16
        self.print_estimated_time(filtered_ids, scrap_per_min)
        self.start_urls = [f'{self.start_url}/{id}' for id in filtered_ids]
        # self.logger.info(" self.start_urls : %s", self.start_urls)
        # DEBUG DO NOT UNCOMMENT
        # self.start_urls = ["https://www.wakfu.com/fr/mmorpg/encyclopedie/armures/2021"]
        # self.start_urls = ["https://www.wakfu.com/fr/mmorpg/encyclopedie/armes/23093"]
        # print (self.start_urls)
        # DEBUG DO NOT UNCOMMENT
        super(ItemDataSpider, self).__init__(*args, **kwargs)



    def print_estimated_time(self, ids, scrap_per_min):
        print("Numbers of url to crawl : ", len(ids))
        if math.ceil(len(ids) / scrap_per_min) > 100:
            min = len(ids) / scrap_per_min
            h = min//60
            m = min % 60
            if h > 1:
                print("Estimated time of scrapping :", h, "hrs", m, "mn")
            else:
                print("Estimated time of scrapping :", h, "hr", m, "mn")
        else:
            print("Estimated time of scrapping : ", math.ceil(len(ids) / scrap_per_min), "mn")

    def parse(self, response):
        if response.status == 200:
            self.logger.info("---Processing URL: %s", response.url)
            # used to write page HTML to file for debug

            # filename = 'raw_html_content.html'
            # with open(filename, 'w', encoding='utf-8') as file:
            #     file.write(response.text)
            #     self.logger.info("Raw HTML content written to %s", filename)

            # main container div showing the drop rates
            panel_content = response.css(
                '.ak-panel-title:contains("Peut être obtenu sur") + .ak-panel-content')

            # check if item can drop
            # if panel_content:
            #     self.logger.info("---panel_content exists")
            # else:
            #     self.logger.warning(
            #         f"Skipping URL: {response.url}, item has no droprates")
            #     return

            # rarity class , used to get the rarity number in case problems with IDs arise
            rarity_class = response.css(
                '.ak-object-rarity span::attr(class)').get()
            rarity_number = re.search(
                r'\d+', rarity_class).group() if rarity_class else None  # type: ignore

            # self.logger.info("Rarity Class: %s", rarity_class)
            self.logger.info("Rarity Number: %s", rarity_number)
            self.logger.info("Item URL: %s", response.url)

            # div showing the droprates
            monster_divs = panel_content.css(
                '.row.ak-container .ak-column.ak-container.col-xs-12.col-md-6 .ak-list-element')
            # self.logger.info("---monster_divs : %s", monster_divs)

            droprates = {}

            for monster_html in monster_divs.extract():

                monster_selector = scrapy.Selector(text=monster_html)
                # Extract monster name
                monster_name = monster_selector.css(
                    '.ak-title span::text').get().strip()  # type: ignore
                self.logger.info("---monster_name : %s", monster_name)

                monster_id_url = monster_selector.css(
                    '.ak-title a::attr(href)').get()
                monster_id_match = re.search(r'/(\d+)-', monster_id_url) if monster_id_url else None
                monster_id = monster_id_match.group(1) if monster_id_match else None
                self.logger.info("---monster_id : %s", monster_id)

                # Extract drop rate
                drop_rate = monster_selector.css(
                    '.ak-aside::text').get().strip()  # type: ignore
                self.logger.info("---drop_rate : %s", drop_rate)

                # Add the monster and drop rate to the dictionary
                droprates[monster_name] = {"drop_rate" : drop_rate, "monster_id" : int(monster_id)} #type: ignore

            title = response.css('title::text').get()
            item_name = title.split(' - ')[0].strip()
            self.logger.info("---item_name : %s", item_name)

            item_id = response.url.split('/')[-1]
            self.logger.info("---item_id : %s", item_id)

            # Append the result
            self.results.append({
                'item': {
                    'name': item_name,
                    'id': item_id,
                },
                'rarity': rarity_number,
                'droprates': droprates,
                'item_url': response.url
            })
        else:
            self.log(
                f"Page not found: {response.url}, error = {response.status}")
            return
        
            
    def closed(self, reason):
        current_category_name = self.get_category_name(self.category_id)
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ScrappedData', f'{current_category_name}_scrapped_data.json')
        # save the scraped data
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.results, file, ensure_ascii=False, indent=2)  # type: ignore
