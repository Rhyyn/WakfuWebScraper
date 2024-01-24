# Disclaimer

This is a personal project for educational and non-commercial purposes. The data obtained through web scraping from wakfu.com is used to make a better encyclopedia for the game users.
All data obtained from the Ankama Studio website is their property.

As the creator, I am not liable for any misuse or violation of terms by users. Use it responsibly and in accordance with the terms and conditions of wakfu.com.

This project is not affiliated with or endorsed by Ankama Studio.
If Ankama Studio has any concerns regarding this project, please contact me directly and I will have it removed shortly.

### ONLY TO BE USED FOR EDUCATIONAL / DEMONSTRATIONAL PURPOSES AND NON-COMMERCIAL PURPOSES

# Explanation

This project is a Scrapy webscraper for wakfu.com, it can scrap monsters data and items, use it to format the data provided by Ankama while including better infos like monsters droprates
This project was developed by myself for the sole reason of patching the gaps in the JSON data Ankama provides


First we need to scrap the list of monsters to get a list with every monster ID, we can then use those IDs to scrap each Monster page.

But why do we need to scrap Monsters before anything else you ask ?

Well because we want the Items drop rates, and the only way to get them is to scrap the monster drops on their pages!

![drops list example](https://i.imgur.com/wClnI3M.png)

We then proceed to use the data we get from the monsters's pages and the items's pages to combine with the provided data by Ankama inside /ScrapyProject/StaticData/items.json

In order to recreate every item with the newly scraped data which lets us add droprates for example :

```
"droprates": {
        "fr": {
            "Erpel": {
                "drop_rate": "1%",
                "monster_id": "5447"
            }
```

# Why half english/french
Well.. because I did not take the time to make language dynamic, since we don't really care about what language we scrap in since we're only interested in the values.

We can get the localized strings by formatting the scraped data with the given data by Ankama, and we end up reconstructing our items data with both FR/EN, this also means that ES/PT is not supported, sorry!

See :
```
  "title": {
          "fr": "Porte-Bonheur d'Eenca",
          "en": "Enca's Lucky Charm"
  }
```
# Running the scripts :
``` bash
git clone / cd inside
```
```
pip install -r requirements.txt
```
### TO RUN DEMO USE:
```
python cli.py test-scrap   
```
(outputs to ScrapedData/ScrapedFiles/ScrapTests) ~1min waiting time

To see the commands use :
```
python cli.py 
```
To list the spiders and their usage :
```
python cli.py list-spiders 
```
To use a spider : (ex monsters_data) and follow the CLI prompts
```
python cli.py crawl monsters_data
```

1. monsters_ids spider needs to be run before monsters_data

2. monsters_data needs to be run before items_data

3. After Scraping monsters_ids, monsters_data and items_data, you can (should) run format_items.py inside /ScrapyProject/ScrapedData


Follow the CLI prompts!
```
cd .\ScrapyProject\ScrapedData\
python format_items.py
```
+ Formatting Preview for Items :
[Before](https://github.com/Rhyyn/WakfuWebScraper/blob/main/ScrapyProject/FormattingPreview/old_format.json) || [After](https://github.com/Rhyyn/WakfuWebScraper/blob/main/ScrapyProject/FormattingPreview/new_format.json)

+ Preview for Monster_IDs :
[Monster_IDs_Preview](https://github.com/Rhyyn/WakfuWebScraper/blob/main/ScrapyProject/FormattingPreview/monsters_IDs_preview.json)

+ Preview for Monsters_data :
[Monster_IDs_Preview](https://github.com/Rhyyn/WakfuWebScraper/blob/main/ScrapyProject/FormattingPreview/monsters_data_preview.json)



# Bugs ? Data missing ?
[Start an issue here](https://github.com/Rhyyn/WakfuWebScraper/issues)



## TODO : 

+ Add language support for categories names, currently categories are display in FR because we don't actually need to scrap any localized strings, only values that we use to match the data Ankama is giving us to create both the FR/EN version with the scrapped values.
+ Refactor JSON_parser, contains a lot of for loops for debug/testing of the data, need to extract them to separate functions for readability 
+ Refactor start of scrap spider with more arguments, like a specific ID / name would be great
+ Adding support for tab completion / arrows keys movement for the CLI prompts
+ Adds Logs for errors
+ Add a formatting option to format ALL files in the ScrapedItems folder

