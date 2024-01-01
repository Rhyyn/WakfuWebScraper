from curses import panel
from unicodedata import category
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
    
    # USED FOR TESTING DO NOT UNCOMMENT
    # ids = [14186, 24130, 24131, 24132, 24133, 24134, 24135, 24136, 24137, 24138, 25793, 25794, 25795, 25796, 25797, 25798, 25799, 25800, 25801, 25802, 27111, 27112, 27113, 27114, 27115, 27116, 27117, 27118, 27119, 27120, 27121, 27122, 27123, 27124, 27125, 27126, 27127, 27128, 27129, 27130, 27131, 27132, 27133, 27134, 27135, 27136, 27137, 27138, 27139, 27140, 27141, 27142, 27143, 27144, 27145, 27146, 27147, 27148, 27149, 27150, 27151, 27152, 27153, 27154, 27155, 27156, 27157, 27158, 27159, 27160, 27161, 27162, 27163, 27164, 27186, 27187, 27188, 27189, 27190, 27191, 27192, 27193, 27194, 27195, 27282, 27957, 27958, 27959, 27960, 28383, 28384, 28385, 28386, 28387, 28388, 28389, 28390, 28798, 28799, 28800, 28801, 28802, 28803, 28804, 28805, 28806, 28807, 28808, 28809, 28810, 28811, 28812, 28813, 28814, 28815, 28816, 28817, 28818, 28819, 28822, 28823, 28824, 28825, 28826, 28827, 28828, 28829, 28830, 28831, 28832, 28833, 28834, 28835, 28836, 28837, 28838, 28839, 28840, 28841, 28842, 28843, 28844, 28845, 28846, 28847, 28848, 28849, 28850, 28851, 28852, 28853, 28854, 28855, 28856, 28857, 28858, 28859, 28860, 28861, 28862, 28863, 28864, 28865, 28866, 28867, 28868, 28869, 28870, 28871, 28872, 28873, 28874, 28875,
    #     28876, 28877, 28878, 28879, 28880, 28881, 28882, 28883, 28884, 28885, 28886, 28887, 28888, 28889, 28890, 28891, 28892, 28893, 28894, 28895, 28896, 28897, 28898, 28899, 28900, 28901, 28902, 28903, 28904, 28905, 28906, 28907, 28908, 28909, 28910, 28911, 28912, 28913, 28914, 28915, 28916, 28917, 28918, 28919, 28920, 28921, 28922, 28923, 28924, 28925, 28926, 28927, 28928, 28929, 28930, 28931, 28932, 28933, 28942, 28943, 28944, 28988, 28989, 28990, 28991, 28992, 28993, 28994, 28995, 28996, 28997, 28998, 28999, 29000, 29001, 29002, 29003, 29004, 29005, 29006, 29007, 29008, 29009, 29495, 29496, 29497, 29498, 29499, 29500, 29504, 29505, 29506, 29507, 29508, 29509, 29510, 29511, 29512, 29513, 29514, 29515, 29591, 29592, 29593, 29871, 29872, 29873, 29874, 29875, 29876, 30737, 30738, 30739, 30740, 30741, 30742, 30743, 30744, 30745, 30746, 30747, 30748, 30749, 30750, 30751, 30752, 30753, 30754, 30763, 30764, 30765, 30946, 30947, 30948, 30949, 30950, 30951, 30952, 30953, 30954, 30955, 30956, 30957, 30958, 30959, 30960, 30961, 30962, 30963, 30964, 30965, 30966, 30967, 30968, 30969, 30970, 30971, 30972, 30973, 30974, 30975, 30993, 30994, 30995, 30996, 30997, 30998, 30999, 31000, 31001, 31002, 31003, 31004]
    # ids = [2037, 2058, 2198, 3812]

    # start_urls = [
    #     'https://www.wakfu.com/fr/mmorpg/encyclopedie/ressources/{}'.format(id) for id in ids]
    
    
    start_urls = []
    results = []
    def get_starting_url(self, category_id, url_mapping):
        category_id = int(category_id)
        base_url = 'https://www.wakfu.com/fr/mmorpg/encyclopedie/'
        category_url = url_mapping.get(category_id, 'Unknown Category')
        return f'{base_url}{category_url}'


    def get_category_name(self, category_id):
        # url_mapping = self.get_id_mappings()
        # category_name = url_mapping.get(category_id, 'Unknown Category')
        item_type_mapping = {
            120: 'amulette', 103: 'anneau', 119: 'bottes', 132: 'cape', 134: 'casque', 133: 'ceinture', 138: 'epaulettes', 136: 'plastron',
            254: 'arme1main', 108: 'arme1main', 110: 'arme1main', 115: 'arme1main', 113: 'arme1main', 223: 'arme2main', 114: 'arme2main', 101: 'arme2main', 111: 'arme2main', 253: 'arme2main', 117: 'arme2main', 112: 'secondemain', 189: 'secondemain',
            646: 'emblemes', 480: 'torches',537: 'outils',
            812: 'sublimation',
            611: 'montures',
            582: 'familiers',
        }
        category_name = item_type_mapping.get(category_id, 'Unknown Category')
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

    def __init__(self, category_id=None, *args, **kwargs):
        
        url_mapping = self.get_id_mappings()
        self.category_id = int(category_id) #type: ignore
        # print("self.category_id", self.category_id)
        self.start_url = self.get_starting_url(self.category_id, url_mapping)
        # print("self.start_url", self.start_url)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        items_json_path = os.path.join(parent_dir, 'items.json')
        with open(items_json_path, 'r', encoding='utf-8') as file:
            items_data = json.load(file)
            
        filtered_ids = [item['definition']['item']['id'] 
                        for item in items_data if item.get('definition', {})
                                                        .get('item', {})
                                                        .get('baseParameters', {})
                                                        .get('itemTypeId') == self.category_id] #type: ignore

        self.logger.info("Filtered Items: %s", filtered_ids)
        scrap_per_min = 16
        self.print_estimated_time(filtered_ids, scrap_per_min)
        self.start_urls = [
            f'{self.start_url}/{id}' for id in filtered_ids
        ]
        # DEBUG DO NOT UNCOMMENT
        # self.start_urls = ["https://www.wakfu.com/fr/mmorpg/encyclopedie/armures/2021"]
        # print (self.start_urls)
        # DEBUG # DEBUG DO NOT UNCOMMENT
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
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'ScrappedData', f'{current_category_name}_scraped_data.json')
        # save the scraped data
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.results, file, ensure_ascii=False, indent=2)  # type: ignore
