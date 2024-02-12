import scrapy
import json
import os
import re


class RessourcesDataSpider(scrapy.Spider):
    """
    -INFO-
    Spider to retrieve all the ressources data.
    -------
    -USAGE-
    python -m cli crawl resources_data
    -------
    -OUTPUT-
    resources_data.json
    --------
    """

    name = "ressources_data"
    allowed_domains = ["wakfu.com"]
    results = []
    ressources_ids = []

    def __init__(self, *args, **kwargs):
        super(RessourcesDataSpider, self).__init__(*args, **kwargs)
        project_dir = os.path.abspath(os.getcwd())
        scraped_ressources_dir = os.path.join(
            project_dir,
            "ScrapyProject",
            "ScrapedData",
            "ScrapedFiles",
            "ScrapedRessources",
        )
        self.ressources_ids_path = os.path.join(
            scraped_ressources_dir, "ressources_IDs.json"
        )
        scraped_ressources_data_path = os.path.join(
            scraped_ressources_dir, "en_ressources_data.json"
        )  # change this when scrapping in english/french
        self.start_urls = self.construct_start_urls()
        self.ressources_ids: list[int] = []

    def construct_start_urls(self):
        with open(self.ressources_ids_path, "r") as file:
            self.ressources_ids = json.load(file)
        # FR
        return [
            "https://www.wakfu.com/fr/mmorpg/encyclopedie/ressources/{}".format(id)
            for id in self.ressources_ids
        ]
        # # EN
        # return [
        #     "https://www.wakfu.com/en/mmorpg/encyclopedia/resources/{}".format(id)
        #     for id in self.ressources_ids
        # ]

    def parse(self, response):
        resource_id = response.url.split("/")[-1]
        if response.status == 200:
            request_headers = response.request.headers
            request_body = response.request.body
            self.logger.info("---Request_headers: %s", request_headers)
            self.logger.info("---Request_body: %s", request_body)
            self.logger.info("---Processing URL: %s", response.url)
            self.logger.info("---Processing CSS: %s", response.css)
            # self.logger.info("response body: %s", response.body)
            # self.logger.info("HTML Content:\n%s", response.text)
            # self.logger.info("Page found: %s", response)
            ressource_level = (
                response.css(".ak-encyclo-detail-level::text").get().strip()
            )
            match = re.search(r"\d+", ressource_level)
            ressource_level = int(match.group()) if match else None
            ressource_title = response.css("h1.ak-return-link::text").getall()
            ressource_title = " ".join(ressource_title).strip()
            rarity_class = response.css(".ak-object-rarity span::attr(class)").get()
            rarity_number = (
                re.search(r"\d+", rarity_class).group() if rarity_class else None
            )
            img_src = response.css("div.ak-encyclo-detail-illu img::attr(src)").get()
            gfxId = None
            if img_src:
                parts = img_src.split("/")
                gfxId = parts[-1].split(".")[0]

            self.logger.info(f"Resource Level: {ressource_level}")
            self.logger.info(f"Resource Title: {ressource_title}")
            self.logger.info(f"Resource Rarity: {rarity_number}")
            self.logger.info(f"Resource gfxId: {gfxId}")
            self.logger.info(f"Resource ID: {resource_id}")

            self.results.append(
                {
                    "id": int(resource_id),
                    "level": ressource_level,
                    "title": ressource_title,
                    "rarity": int(rarity_number),
                    "gfxId": int(gfxId),
                }
            )

            # DEBUGGGGGG
            # elements = response.css("body").getall()
            # file_path = os.path.join(
            #     os.path.dirname(os.path.realpath(__file__)),
            #     "..",
            #     "ScrapedData",
            #     "scrapedFiles",
            #     "ScrapedRessources",
            #     "css_selector.html",
            # )
            # with open(file_path, "w") as f:
            #     f.write("\n".join(elements))
            # self.logger.info("CSS selector results written to %s", file_path)

        else:
            self.log(f"Page not found: {response.url}, error = {response.status}")
            return

    def closed(self, reason):
        ressources_ids_length = len(self.ressources_ids)
        results_length = len(self.results)
        missing_ids = []
        if results_length < ressources_ids_length:
            print("Some ressources seems to be missing : ")
            for res_id in self.results:
                if res_id not in self.ressources_ids:
                    missing_ids.append(res_id)
            print(missing_ids)

        file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "ScrapedData",
            "scrapedFiles",
            "ScrapedRessources",
            "fr_ressources_data.json",
        )
        # save the scraped data
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.results, file, ensure_ascii=False, indent=2)  # type: ignore
