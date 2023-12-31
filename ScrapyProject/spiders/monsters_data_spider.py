import scrapy
import json
import os
import re
from ScrapyProject.middlewares import RotateUserAgentMiddleware

#--- WARNING ---#
#--- WARNING ---#
#--- WARNING ---#
#--- MAKE SURE TO RUN python -m cli crawl monster_urls ---#
#--- BEFORE RUNNING THIS SPIDER ---#
#--- OTHERWISE SOME MONSTERS MIGHT BE MISSING ---#



class MonstersDataSpider(scrapy.Spider):
    """
    -INFO-
    Spider to retrieve all the info about the monsters.
    -------
    -USAGE-
    python -m cli crawl monsters_data
    -------
    -OUTPUT-
    monsters_stats_data.json
    --------
    """
    name = "monsters_data"
    allowed_domains = ["wakfu.com"]
    start_urls = ["https://wakfu.com"]
    results = []
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    monster_IDs_path = os.path.join(parent_dir, 'monsters_IDs.json')
    monsters_IDs = []
    

    def __init__(self, *args, **kwargs):
        super(MonstersDataSpider, self).__init__(*args, **kwargs)
        self.start_urls = self.construct_start_urls()
        # # TESTING 
        # test_IDS = ["4718", "2710", "4228", "4381", "4726", "2351", "2340", "4725", "4230"]
        # self.start_urls = [
        #     'https://www.wakfu.com/fr/mmorpg/encyclopedie/monstres/{}'.format(id) for id in test_IDS]

    def construct_start_urls(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
        monster_IDs_path = os.path.join(parent_dir, 'monsters_IDs.json')

        with open(monster_IDs_path, 'r') as file:
            monsters_IDs = json.load(file)

        return [
            'https://www.wakfu.com/fr/mmorpg/encyclopedie/monstres/{}'.format(id) for id in monsters_IDs
        ]


    def parse(self, response):
        if response.status == 200:
            self.logger.info("---Processing URL: %s", response.url)

            # monster_name
            title = response.css('title::text').get()
            monster_name = title.split(' - ')[0].strip()

            # monster_famille
            monster_famille = response.css(
                'div.col-xs-8.ak-encyclo-detail-type > span::text').get()
            self.logger.info("monster_famille : %s", monster_famille)
            if monster_famille is None:
                monster_famille = "Unknown"

            # monster_level
            monster_level = response.css('div.ak-encyclo-detail-level::text').get()

            # is_monster_capturable
            is_monster_capturable = response.css(
                'div.catchable strong::text').get()
            
            # monster_id
            monster_id = response.url.split('/')[-1]


            # monster_charas (it's stats)
            monster_charas = []
            charas_container_div = response.css(
                'body > div.ak-mobile-menu-scroller > div.container.ak-main-container > div > div > div > main > div.ak-container.ak-main-center > div > div:nth-child(3) > div > div > div.col-sm-10 > div > div.row.ak-nocontentpadding > div:nth-child(1) > div > div.ak-panel-content > div')

            for ak_list_element in charas_container_div.css('div.ak-list-element'):
                # Extract information from div with class "ak-title" inside each ak-list-element
                title_div = ak_list_element.css('div.ak-title::text').get()
                value_span = ak_list_element.css('div.ak-title span::text').get()

                # Check if both title_div and value_span are not None
                if title_div and value_span:
                    monster_charas.append({title_div.strip(): value_span.strip()})


            # monster_resists (it's stats offensive / defensive stats)
            monster_resists = []
            resists_container_div = response.css(
                'body > div.ak-mobile-menu-scroller > div.container.ak-main-container > div > div > div > main > div.ak-container.ak-main-center > div > div:nth-child(3) > div > div > div.col-sm-10 > div > div.row.ak-nocontentpadding > div:nth-child(2) > div div.ak-panel-content > div')
            
            for ak_list_element in resists_container_div.css('div.ak-list-element'):
                resist_name_div = ak_list_element.css(
                    'div.ak-aside span.ak-icon-small::text').get()

                if resist_name_div:
                    resist_name = resist_name_div.strip()
                    boost_value = ak_list_element.css(
                        'div.ak-content div.ak-title span.ak-boost + span::text').get().strip()
                    resist_value = ak_list_element.css(
                        'div.ak-content div.ak-title span.ak-resist + span::text').get().strip()

                    monster_resists.append({
                        resist_name: {
                            'monster_attack_boost': boost_value,
                            'monster_resist': resist_value
                        }
                    })

            # monster_drops (If the monster can drop items)
            monster_drops = {}
            # check if monster has drops
            drops_panel_content = response.css(
                '.ak-panel-title:contains("Drops") + .ak-panel-content')

            if drops_panel_content:
                self.logger.info("panel_content exists")
                items_drop_divs = drops_panel_content.css('.row.ak-container .ak-column.ak-container.col-xs-12.col-md-6 .ak-list-element')
            
                for item__drop_divs_html in items_drop_divs.extract():

                    item_selector = scrapy.Selector(text=item__drop_divs_html)
                    item_name = item_selector.css(
                        '.ak-title span::text').get().strip()  # type: ignore
                    self.logger.info("---item_name : %s", item_name)

                    # get rarity as number
                    rarity_class = response.css(
                        '.item-rarity span::attr(class)').get()
                    rarity_number = re.search(
                        r'\d+', rarity_class).group() if rarity_class else None  # type: ignore

                    # get level of item as numeric value (strips Niv.)
                    level_div = item_selector.css('div.ak-aside::text').get()
                    item_numeric_level = 0
                    if level_div:
                        level_match = re.search(r'\d+', level_div)
                        if level_match:
                            item_numeric_level = level_match.group()

                    image_url = item_selector.css('div.ak-content div.ak-title a::attr(href)').get()
                    self.logger.info("---image_url : %s", image_url)
                    item_drop_name = item_selector.css('div.ak-content div.ak-title span.ak-linker::text').get()
                    item_drop_rarity = rarity_number
                    item_drop_chance = item_selector.css('div.ak-text div.ak-drop-percent span:nth-child(2)::text').get()
                    item_drop_level = item_numeric_level
                    item_id_match = re.search(r'/(\d+)-', image_url) if image_url else None
                    item_id = item_id_match.group(1) if item_id_match else None

                    current_item = {
                            "item_drop_chance": item_drop_chance.strip() if item_drop_chance else None,
                            "item_drop_rarity": item_drop_rarity.strip() if item_drop_rarity else None,
                            "item_drop_level": item_drop_level.strip() if item_drop_level else None,
                            "item_id" : item_id
                            }
                    monster_drops[item_drop_name] = current_item
            else:
                self.logger.info("drops_panel_content not found")


            self.logger.info("monster_name: %s", monster_name)
            self.logger.info("monster_id: %s", monster_id)
            self.logger.info("monster_famille: %s", monster_famille)
            self.logger.info("monster_level: %s", monster_level)
            self.logger.info("is_monster_capturable: %s", is_monster_capturable)
            self.logger.info("monster_charas: %s", monster_charas)
            self.logger.info("monster_resists: %s", monster_resists)
            self.logger.info("drops: %s", monster_drops)


            # Append the result
            self.results.append({
                'monster_name': monster_name,
                'monster_id' : monster_id,
                'monster_famille': monster_famille,
                'monster_level': monster_level,
                'is_monster_capturable': is_monster_capturable,
                'monster_charas': monster_charas,
                'monster_resists': monster_resists,
                'drops': monster_drops
            })
        else:
            self.log(
                f"Page not found: {response.url}, error = {response.status}")
            return


    def closed(self, reason):
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'Output', 'monsters_stats_data.json')
        # save the scraped data
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.results, file, ensure_ascii=False, indent=2)  # type: ignore