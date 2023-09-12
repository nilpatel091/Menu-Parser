import json
with open('ubereats/uber_eats_items.json') as items:
    items_data = json.load(items)

with open('ubereats/uber_eats_menustructure.json') as menu_structure:
    menu_structure_data = json.load(menu_structure) 

with open('ubereats/customizations.json') as modifiers_structure:
    modifiers_structure_data = json.load(modifiers_structure)

menu = {}
menu["items"]  = {}


#modifiers
menu["modifiers"] = {}
for uuid, modifier_data in modifiers_structure_data["customizationsMap"].items():
    menu["modifiers"][uuid] = {}
    menu["modifiers"][uuid]["title"] = modifier_data["title"]["defaultValue"]
    menu["modifiers"][uuid]["description"] = None
    menu["modifiers"][uuid]["price"] = None
    menu["modifiers"][uuid]["image_url"] = None



#items 
for uuid, item_data in items_data["itemsMap"].items():
    menu["items"][uuid] = {}
    menu["items"][uuid]["title"] = item_data["itemInfo"]["title"]["defaultValue"]
    menu["items"][uuid]["description"] = None
    menu["items"][uuid]["price"] = item_data["paymentInfo"]["priceInfo"]["defaultValue"]["price"]["low"]
    
    menu["items"][uuid]["modifiers"] = []
    if "description" in item_data["itemInfo"]:
        if "defaultValue" in item_data["itemInfo"]["description"]:
            menu["items"][uuid]["descrtipion"] = item_data["itemInfo"]["description"]["defaultValue"]  

    if "image" in item_data["itemInfo"]:
        if "imageURL" in item_data["itemInfo"]["image"]:
            menu["items"][uuid]["image_url"] = item_data["itemInfo"]["image"]["imageURL"]
    else:
        menu["items"][uuid]["image_url"] = None
    
    if "customizationUUIDs" in item_data["itemInfo"]:
        for modifier_uuid in item_data["customizationUUIDs"]["defaultValue"]:
            menu["items"][uuid]["modifiers"].append(menu["modifiers"][modifier_uuid])

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

with open("ubereats_formatted_menu.json","w") as file:
    json.dump(menu, file, indent=4)


