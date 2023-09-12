import json

with open("grubhub_menu.json", "r") as menu:
    data = json.load(menu)
    
response = data
menu = {}

#modifiers
menu["modifiers"] = {}
for modifier in response["modifier_prompts"]:
    modifier = modifier["latest_version"]
    new_modifier = {}
    new_modifier["title"] = modifier["name"]
    new_modifier["description"] = None
    new_modifier["price"] = None
    new_modifier["image_url"] = None
    menu["modifiers"][modifier["uuid"]] = new_modifier

#items
items = {}

for item in response["items"]:
    item = item["latest_version"]
    new_item = {}
    new_item["title"] = item["name"]
    if "price" in item:
        new_item["price"] = item["price"]
    elif "price_variations" in item:
        new_item["price"] = item["price_variations"]["maximum_price"]
    new_item["description"] = item["description"]
    new_item["image_url"] = None
    new_item["modifiers"] = []
    for modifier in item["modifier_prompts"]:
        new_item["modifiers"].append(menu["modifiers"][modifier])

    items[item["uuid"]] = new_item

menu["items"] = items

#categories
categories = {}
for category in response["menu_sections"]:
    category = category["latest_version"]
    new_category = {}
    new_category["title"] = category["name"]
    new_category["subtitle"] = None
    new_category["description"] = category["description"]
    new_category["items"] = []
    for item_uuid in category["items"]:
        item = menu["items"]
        new_category["items"].append(menu["items"][item_uuid])
        del menu["items"][item_uuid]

    new_category["description"] = category["description"]
    categories[category["uuid"]] = new_category
    

menu["categories"] = categories

#menu
menu["menu"] = { "title":"title", "type": None,  }
menu["menu"]["categories"] = []
for section in response["menu_info"]["latest_version"]["sections"]:
    menu["menu"]["categories"].append(menu["categories"][section])
    del menu["categories"][section]

del menu["items"]
del menu["categories"]
del menu["modifiers"]

with open("formatted_menu.json","w") as file:
    json.dump(menu, file, indent=4)




