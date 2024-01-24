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
    Inside the ScrapedData Folder
    --------
    """
    name = 'items_data'
    start_urls = []
    results = []

    def get_starting_url(self, category_id: int, url_mapping):
        if not category_id:
            raise ValueError("Empty category_id")

        # param gets converted to str for some reason
        # need to convert it back to int | :)
        category_id = int(category_id)
        base_url = 'https://www.wakfu.com/fr/mmorpg/encyclopedie/'
        category_url = url_mapping.get(category_id, 'Unknown Category')

        return f'{base_url}{category_url}'

    def get_matching_ids(self, category_id):
        category_id = int(category_id)
        item_type_mapping = {
            120: 'amulette', 103: 'anneau', 119: 'bottes', 132: 'cape', 134: 'casque', 133: 'ceinture', 138: 'epaulettes', 136: 'plastron',
            254: 'arme1main', 108: 'arme1main', 110: 'arme1main', 115: 'arme1main', 113: 'arme1main', 223: 'arme2main', 114: 'arme2main', 101: 'arme2main', 111: 'arme2main', 253: 'arme2main', 117: 'arme2main', 112: 'secondemain', 189: 'secondemain',
            646: 'emblemes', 480: 'torches', 537: 'outils',
            812: 'sublimation',
            611: 'montures',
            582: 'familiers',
        }
        category_name = item_type_mapping.get(category_id)
        categories_to_scrap: list[int] = []
        for item_type_id, name_item in item_type_mapping.items():
            if category_name == name_item:
                categories_to_scrap.append(item_type_id)

        if category_name is None:
            raise ValueError(f"Invalid category ID: {category_id}")

        return categories_to_scrap

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
            646: 'accessoires', 480: 'accessoires', 537: 'accessoires',
            812: 'ressources',
            611: 'montures',
            582: 'familiers',
        }
        return url_mapping
    
    def get_ids_list(self, categories_to_scrap: list[int], items_data):
        new_ids: list[int] = []
        for category_id in categories_to_scrap:
            for item in items_data:
                if item['definition']['item']['baseParameters']['itemTypeId'] == category_id:
                    new_ids.append(item['definition']['item']['id'])
        return new_ids

    def construct_urls(self, start_url: str, new_ids:list[int]):
        scrap_per_min = 16
        self.print_estimated_time(new_ids, scrap_per_min)
        start_urls = [f'{start_url}/{id}' for id in new_ids]
        return start_urls

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
            
    

    def __init__(self, category_id: int, *args, **kwargs):
        # param gets converted to str for some reason
        # need to convert it back to int | :)
        self.logger.info("ItemDataSpider !")
        self.category_id = int(category_id)
        categories_to_scrap = self.get_matching_ids(category_id)
        url_mapping = self.get_id_mappings()
        self.start_url = self.get_starting_url(self.category_id, url_mapping)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        static_data_dir_path = os.path.join(parent_dir, 'StaticData')
        items_json_path = os.path.join(static_data_dir_path, 'items.json')
        with open(items_json_path, 'r', encoding='utf-8') as file:
            items_data = json.load(file)

        self.new_ids = self.get_ids_list(categories_to_scrap, items_data)
        urls = self.construct_urls(self.start_url, self.new_ids)
        self.start_urls = urls
        print(self.start_urls)
        # DEBUG DO NOT UNCOMMENT
        super(ItemDataSpider, self).__init__(*args, **kwargs)

    # def start_requests(self):
    #     self.logger.info("start_requests called")
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}, meta={'handle_httpstatus_list': [301, 302]})

    def parse(self, response):
        if response.status == 302 and 'Location' in response.headers:
            redirected_url = response.headers['Location'].decode('utf-8')
            self.logger.warning("Redirected to %s. Handling redirection.", redirected_url)
            
            if redirected_url != response.url:
                yield scrapy.Request(redirected_url, callback=self.parse, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}, meta={'original_url': response.url})
            else:
                self.logger.error("Redirect loop detected for URL %s", response.url)
            return
        
        if response.status == 200:
            self.logger.info("---Processing URL: %s", response.url)
            # self.logger.debug("Response body: %s", response.body)
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
                monster_id_match = re.search(
                    r'/(\d+)-', monster_id_url) if monster_id_url else None
                monster_id = monster_id_match.group(
                    1) if monster_id_match else None
                self.logger.info("---monster_id : %s", monster_id)

                # Extract drop rate
                drop_rate = monster_selector.css(
                    '.ak-aside::text').get().strip()  # type: ignore
                self.logger.info("---drop_rate : %s", drop_rate)

                # Add the monster and drop rate to the dictionary
                droprates[monster_name] = {
                    "drop_rate": drop_rate, "monster_id": int(monster_id)}  # type: ignore

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
            self.logger.info(
                f"Page not found: {response.url}, error = {response.status}")
            return

    def closed(self, reason):
        current_category_name = self.get_category_name(self.category_id)
        selected_ids_length = len(self.new_ids)
        results_length = len(self.results)
        missing_ids = []
        if results_length < selected_ids_length:
            print("Some items seems to be missing :")
            for res_id in self.results:
                if res_id not in self.new_ids:
                    missing_ids.append(res_id)
            print(missing_ids) 

        file_path = os.path.join(os.path.dirname(os.path.realpath(
            __file__)), '..', 'ScrapedData', 'ScrapedFiles', 'ScrapedItems', f'{current_category_name}_scraped_data.json')
        # save the scraped data
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.results, file, ensure_ascii=False,
                      indent=2)  # type: ignore
