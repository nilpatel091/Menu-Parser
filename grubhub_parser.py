import json

with open("grubhub_menu.json", "r") as menu:
    data = json.load(menu)

with open("grubhub_content.json","r") as menu:    
    content_data = json.load(menu)

grubhub_menu = data
grubhub_menu_media = content_data
menu = dict()

menu["images"] = {}

for content in grubhub_menu_media["contents"]:
    if content["entity_type"] == "menu_item":
        menu["images"][content["entity_uuid"]] = {}
        menu["images"][content["entity_uuid"]]["image_url"] = content[
            "secure_url"
        ]


# modifiers
menu["modifiers"] = {}
for modifier in grubhub_menu["modifiers"]:
    modifier = modifier["latest_version"]
    new_modifier = dict()
    new_modifier["name"] = modifier["name"]
    new_modifier["description"] = modifier["description"]
    new_modifier["price"] = modifier["default_price"]
    new_modifier["sub_modifier_categories"] = []
    new_modifier["image_url"] = None
    new_modifier["modifier_price_info"] = []
    menu["modifiers"][modifier["uuid"]] = new_modifier

menu["modifier_lists"] = {}
for modifier_list in grubhub_menu["modifier_lists"]:
    menu["modifier_lists"][modifier_list["uuid"]] = modifier_list

# size_prompts
menu["size_prompts"] = {}
for size_prompt in grubhub_menu["size_prompts"]:
    menu["size_prompts"][size_prompt["uuid"]] = size_prompt

# modifiers_categories
menu["modifier_categories"] = {}
for modifier_category in grubhub_menu["modifier_prompts"]:
    new_modifier_category = dict()
    new_modifier_category["title"] = modifier_category["latest_version"][
        "name"
    ]
    new_modifier_category["image_url"] = None
    new_modifier_category["price"] = None
    new_modifier_category["description"] = None
    new_modifier_category["modifiers"] = []
    for modifier_uuid in menu["modifier_lists"][
        modifier_category["latest_version"]["modifier_list"]
    ]["latest_version"]["modifiers"]:
        new_modifier_category["modifiers"].append(
            menu["modifiers"][modifier_uuid]
        )
    menu["modifier_categories"][
        modifier_category["uuid"]
    ] = new_modifier_category

# items
items = {}
for item in grubhub_menu["items"]:
    item = item["latest_version"]
    new_item = dict()
    new_item["title"] = item["name"]
    new_item["is_archived"] = False
    if "price" in item:
        new_item["price"] = item["price"]
    elif "price_variations" in item:
        new_item["price"] = item["price_variations"]["minimum_price"]
    new_item["description"] = item["description"]
    if item["uuid"] in menu["images"]:
        new_item["image_url"] = menu["images"][item["uuid"]]["image_url"]
    else:
        new_item["image_url"] = None
    new_item["modifier_categories"] = []
    for modifier_category_uuid in item["modifier_prompts"]:
        new_item["modifier_categories"].append(
            menu["modifier_categories"][modifier_category_uuid]
        )
    # add modifier_category in item for size vice price.
    if "size_prompt" in item:
        new_modifier_category = dict()
        new_modifier_category["title"] = menu["size_prompts"][
            item["size_prompt"]
        ]["latest_version"]["name"]
        new_modifier_category["description"] = None
        new_modifier_category["price"] = None
        new_modifier_category["image_url"] = None
        new_modifier_category["modifiers"] = []
        for size_data in menu["size_prompts"][item["size_prompt"]][
            "latest_version"
        ]["sized_prices"]:
            new_modifier = dict()
            new_modifier["name"] = size_data["display_name"]
            new_modifier["price"] = size_data["price"]
            new_modifier["description"] = None
            new_modifier["image_url"] = None
            new_modifier_category["modifiers"].append(new_modifier)
            new_modifier["sub_modifier_categories"] = []

        new_item["modifier_categories"].append(new_modifier_category)
    items[item["uuid"]] = new_item
menu["items"] = items

for item_schedule in grubhub_menu["schedule_overrides"]["item_overrides"]:
    menu["items"][item_schedule["item_id"]]["is_archived"] = True

# categories
categories = {}
for category in grubhub_menu["menu_sections"]:
    category = category["latest_version"]
    new_category = dict()
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

# menu
menu["menu"] = {
    "title": "title_grubhub",
    "type": None,
}
menu["menu"]["categories"] = []
for section in grubhub_menu["menu_info"]["latest_version"]["sections"]:
    menu["menu"]["categories"].append(menu["categories"][section])
    del menu["categories"][section]

del menu["items"]
del menu["categories"]
del menu["modifiers"]
del menu["modifier_categories"]
del menu["modifier_lists"]
del menu["size_prompts"]
menu["menu"]["integration"] = None
with open("grubhub_formatted_menu.json","w") as file:
    json.dump(menu["menu"], file, indent=4)


