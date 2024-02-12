from unicodedata import category
import click
from scrapy.cmdline import execute
from ScrapyProject.spiders.items_data import ItemDataSpider
from ScrapyProject.spiders.monsters_ids_spider import MonstersIdsSpider
from ScrapyProject.spiders.monsters_data_spider import MonstersDataSpider
from ScrapyProject.spiders.test_spider import TestScrapSpider
from ScrapyProject.spiders.ressources_ids_spider import RessourcesIdsSpider
from ScrapyProject.spiders.ressources_data_spider import RessourcesDataSpider

from ScrapyProject.Scripts import run_tests
import sys

# Define the available item types
ITEM_TYPES = ["armures", "armes", "autres"]

# Define armures search categories
ARMURES_CATEGORIES = {
    "amulette": 120,
    "anneau": 103,
    "bottes": 119,
    "cape": 132,
    "casque": 134,
    "ceinture": 133,
    "epaulettes": 138,
    "plastron": 136,
}

ARMES_CATEGORIES = {
    "arme1main": [254, 108, 110, 115, 113],
    "arme2main": [223, 114, 101, 111, 253, 117],
    "secondemain": [112, 189],
}

AUTRES_CATEGORIES = {
    "sublimation": 812,
    "emblemes": 646,
    "familier": 582,
    "montures": 611,
    "torches": 480,
    "outils": 537,
}


# subli ressources
# embleme accessoires
# familiers familiers
# montures montures
# torches accessories
# outils accessoires


ITEM_TYPE_URLS = {
    "armures": "https://www.wakfu.com/fr/mmorpg/encyclopedie/armures/",
    "armes": "https://www.wakfu.com/fr/mmorpg/encyclopedie/armes/",
    "autres": "https://www.wakfu.com/fr/mmorpg/encyclopedie/autres/",
}


SPIDERS = {
    "items_data": ItemDataSpider,
    "monsters_ids": MonstersIdsSpider,
    "monsters_data": MonstersDataSpider,
    "ressources_ids": RessourcesIdsSpider,
    "ressources_data": RessourcesDataSpider,
    "tests": TestScrapSpider,
}


@click.group()
def cli():
    pass


# @click.command() Maybe?
# def select_language():
#     """Available languages"""
#     click.echo("Available Spiders:")


@click.command()
def list_spiders():
    """List available spiders and their purposes."""
    click.echo("Available Spiders:")
    for spider_name, spider_class in SPIDERS.items():
        if spider_name == "tests":
            pass
        purpose = (
            spider_class.__doc__.strip() if spider_class.__doc__ else "No description"
        )
        click.echo(f"{spider_name}: {purpose}")


@click.command()
@click.argument("spider_name")
def crawl(spider_name):
    """Run a Scrapy spider."""
    if spider_name == "items_data":
        crawl_items_data()
    else:
        execute(["scrapy", "crawl", spider_name])


@click.command()
def test_scrap():
    """Run a a single scrap test"""
    category_id: int = 120
    wanted_amount: int = 10
    execute(
        [
            "scrapy",
            "crawl",
            "tests",
            "-a",
            f"category_id={category_id}",
            "-a",
            f"wanted_amount={wanted_amount}",
        ]
    )
    return


# Define a separate function for crawling items_data
def crawl_items_data():
    item_type = click.prompt(
        "What type of items do you want to crawl?", type=click.Choice(ITEM_TYPES)
    )

    if item_type == "armures":
        crawl_armures()
    elif item_type == "armes":
        crawl_armes()
    elif item_type == "autres":
        crawl_autres()
    else:
        print("error with type of items to crawl")


def crawl_armures():
    armure_category = click.prompt(
        "What type of armures do you want to crawl?",
        type=click.Choice(list(map(str, ARMURES_CATEGORIES.keys()))),
    )

    category_id = ARMURES_CATEGORIES.get(armure_category)

    if category_id is not None:
        execute(["scrapy", "crawl", "items_data", "-a", f"category_id={category_id}"])
    else:
        click.echo(f"Invalid selection: {armure_category}")


def crawl_armes():
    arme_category = click.prompt(
        "What type of armes do you want to crawl?",
        type=click.Choice(list(map(str, ARMES_CATEGORIES.keys()))),
    )

    category_id = ARMES_CATEGORIES.get(arme_category)

    if category_id is not None:
        id = category_id[0]
        print("type of id inside my cli is : ", type(id))
        execute(["scrapy", "crawl", "items_data", "-a", f"category_id={id}"])
    else:
        click.echo(f"Invalid selection: {arme_category}")


def crawl_autres():
    autre_category = click.prompt(
        "What type of autres do you want to crawl?",
        type=click.Choice(list(map(str, AUTRES_CATEGORIES.keys()))),
    )

    # Get the corresponding category ID
    category_id = AUTRES_CATEGORIES[autre_category]

    execute(["scrapy", "crawl", "items_data", "-a", f"category_id={category_id}"])


cli.add_command(list_spiders)
cli.add_command(crawl)
cli.add_command(test_scrap)
# cli.add_command(select_language)

if __name__ == "__main__":
    cli()
