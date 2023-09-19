#this code extrat itmeuuid from uber eats uuids.
import json

with open('ubereats/uber_eats_menustructure.json') as menu_structure:
    menu_structure_data = json.load(menu_structure) 

payload1 = {}
payload1["itemUUIDs"] = []
for item_data in menu_structure_data["menuStructure"]["items"]:
    payload1["itemUUIDs"].append(item_data["uuid"])



payload2 = {}
payload2["customizationUUIDs"] = []
for modifier_data in menu_structure_data["menuStructure"]["customizations"]:
    payload2["customizationUUIDs"].append(modifier_data["uuid"])

print(payload1)
print(payload2)
