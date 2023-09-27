import json
with open('ubereats/uber_eats_items.json') as items:
    items_data = json.load(items)

with open('ubereats/uber_eats_menustructure.json') as menu_structure:
    menu_structure_data = json.load(menu_structure) 

with open('ubereats/customizations.json') as modifiers_structure:
    modifier_category_data1 = json.load(modifiers_structure)

menu = {}

item_modifier_category_mapping = {}

for item in menu_structure_data["menuStructure"]["items"]:
    item_modifier_category_mapping[item["uuid"]] = item["defaultCustomizationUUIDs"]



#submodifiers
menu["sub_modifiers"] = {}  
for modifier_uuid, modifier_data in items_data["itemsMap"].items():
    menu["sub_modifiers"][modifier_uuid] = {} 
    menu["sub_modifiers"][modifier_uuid]["name"] = modifier_data["itemInfo"]["title"]["defaultValue"]
    menu["sub_modifiers"][modifier_uuid]["description"] = None  
    menu["sub_modifiers"][modifier_uuid]["image_url"] = None
    if "overrides" in modifier_data["paymentInfo"]["priceInfo"]:
        menu["sub_modifiers"][modifier_uuid]["price"]["low"] = modifier_data["paymentInfo"]["priceInfo"]["overrides"][0]["overriddenValue"]["price"]["low"]
    else:    
        menu["sub_modifiers"][modifier_uuid]["price"] = modifier_data["paymentInfo"]["priceInfo"]["defaultValue"]["price"]["low"]

    if "description" in modifier_data["itemInfo"]:
        if "defaultValue" in modifier_data["itemInfo"]["description"]:
            menu["sub_modifiers"][modifier_uuid]["description"] = modifier_data["itemInfo"]["description"]["defaultValue"]  

    if "image" in modifier_data["itemInfo"]:
        if "imageURL" in modifier_data["itemInfo"]["image"]:
            menu["sub_modifiers"][modifier_uuid]["image_url"] = modifier_data["itemInfo"]["image"]["imageURL"]

#submodifier_categories
menu["sub_modifier_categories"] = {}  
for modifier_category_uuid, modifier_category_data in modifier_category_data1["customizationsMap"].items():
    menu["sub_modifier_categories"][modifier_category_uuid] = {}
    menu["sub_modifier_categories"][modifier_category_uuid]["title"] = modifier_category_data["title"]["defaultValue"]
    menu["sub_modifier_categories"][modifier_category_uuid]["price"] = None
    menu["sub_modifier_categories"][modifier_category_uuid]["image_url"] = None
    menu["sub_modifier_categories"][modifier_category_uuid]["description"] = None
    menu["sub_modifier_categories"][modifier_category_uuid]["sub_modifiers"] = []
    for modifier_uuid in modifier_category_data["options"]:
        menu["sub_modifier_categories"][modifier_category_uuid]["sub_modifiers"].append(menu["sub_modifiers"][modifier_uuid["uuid"]])


#modifiers
menu["modifiers"] = {}
for modifier_uuid, modifier_data in items_data["itemsMap"].items():
    menu["modifiers"][modifier_uuid] = {}
    menu["modifiers"][modifier_uuid]["name"] = modifier_data["itemInfo"]["title"]["defaultValue"]
    menu["modifiers"][modifier_uuid]["description"] = None  
    menu["modifiers"][modifier_uuid]["image_url"] = None
    menu["modifiers"][modifier_uuid]["price"] = modifier_data["paymentInfo"]["priceInfo"]["defaultValue"]["price"]["low"]

    if "description" in modifier_data["itemInfo"]:
        if "defaultValue" in modifier_data["itemInfo"]["description"]:
            menu["modifiers"][modifier_uuid]["description"] = modifier_data["itemInfo"]["description"]["defaultValue"]  

    if "image" in modifier_data["itemInfo"]:
        if "imageURL" in modifier_data["itemInfo"]["image"]:
            menu["modifiers"][modifier_uuid]["image_url"] = modifier_data["itemInfo"]["image"]["imageURL"]
    
    menu["modifiers"][modifier_uuid]["sub_modifier_categories"] = []
    if "customizationUUIDs" in modifier_data:
        for sub_modifier_category_uuid in modifier_data["customizationUUIDs"]["defaultValue"]:
            menu["modifiers"][modifier_uuid]["sub_modifier_categories"].append(menu["sub_modifier_categories"][sub_modifier_category_uuid])


#modifier_categories
menu["modifier_categories"] = {}
for modifier_category_uuid, modifier_category_data in modifier_category_data1["customizationsMap"].items():
    menu["modifier_categories"][modifier_category_uuid] = {}
    menu["modifier_categories"][modifier_category_uuid]["title"] = modifier_category_data["title"]["defaultValue"]
    menu["modifier_categories"][modifier_category_uuid]["price"] = None
    menu["modifier_categories"][modifier_category_uuid]["image_url"] = None
    menu["modifier_categories"][modifier_category_uuid]["description"] = None
    menu["modifier_categories"][modifier_category_uuid]["modifiers"] = []
    for modifier_uuid in modifier_category_data["options"]:
        
        menu["modifier_categories"][modifier_category_uuid]["modifiers"].append(menu["modifiers"][modifier_uuid["uuid"]])


#items 
menu["items"]  = {}
for uuid, item_data in items_data["itemsMap"].items():
    menu["items"][uuid] = {}
    menu["items"][uuid]["title"] = item_data["itemInfo"]["title"]["defaultValue"]
    menu["items"][uuid]["description"] = None
    menu["items"][uuid]["image_url"] = None
    menu["items"][uuid]["is_archive"] = False
    menu["items"][uuid]["price"] = item_data["paymentInfo"]["priceInfo"]["defaultValue"]["price"]["low"]
    menu["items"][uuid]["modifier_categories"] = [] 

    if "description" in item_data["itemInfo"]:
        if "defaultValue" in item_data["itemInfo"]["description"]:
            menu["items"][uuid]["description"] = item_data["itemInfo"]["description"]["defaultValue"]  

    if "image" in item_data["itemInfo"]:
        if "imageURL" in item_data["itemInfo"]["image"]:
            menu["items"][uuid]["image_url"] = item_data["itemInfo"]["image"]["imageURL"]
        

    if item_modifier_category_mapping[uuid]:
        for modifier_category_uuid in item_modifier_category_mapping[uuid]:
            menu["items"][uuid]["modifier_categories"].append(menu["modifier_categories"][modifier_category_uuid])

#categories
menu["categories"] = {}
for uuid, category_data in menu_structure_data["menuStructure"]["subsectionsMap"].items():
    menu["categories"][uuid] = {}
    menu["categories"][uuid]["title"]= category_data["title"]["defaultValue"]
    menu["categories"][uuid]["subtitle"] = None
    menu["categories"][uuid]["description"] = None
    menu["categories"][uuid]["items"] = []
    for item_data in category_data["displayItems"]:
        menu["categories"][uuid]["items"].append(menu["items"][item_data["uuid"]])
    
#menu
menu["menu"] = {}
menu["menu"]["title"] = menu_structure_data["menuStructure"]["sections"][0]["title"]["defaultValue"]
menu["menu"]["type"] = None
menu["menu"]["categories"] = []
 
for uuid,data in menu_structure_data["menuStructure"]["subsectionsMap"].items():
    menu["menu"]["categories"].append(menu["categories"][uuid])

del menu["categories"]
del menu["items"]
del menu["modifiers"]
del menu["modifier_categories"]
del menu["sub_modifiers"]
del menu["sub_modifier_categories"]

with open("ubereats_formatted_menu.json","w") as file:
    json.dump(menu["menu"], file, indent=4)


