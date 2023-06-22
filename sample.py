# print("0 - 5kg"=="0 - 5kg")
#
# # Dictionaries
# dict1 = {'key1': 10, 'key2': 20, 'key3': 30}
# dict2 = {'value1': 'key1', 'value2': 'key2', 'value3': 'key3'}
#
# # Checking if the value of one dictionary matches a key in another dictionary
# value_to_check = 20
# key_to_check = 'value2'
#
# if dict1[dict2[key_to_check]] == value_to_check:
#     print("The value matches the key.")
# else:
#     print("The value does not match the key.")
#
#
# # Creating a dictionary mapping serial numbers to tpl dictionaries
# tpl_mapping = {tpl["serial_number"]: tpl for tpl in tpl_data}
#
# # Updating drones_data using the mapping
# for drone in drones_data:
#     tpl = tpl_mapping.get(drone["serial_number"])
#     if tpl:
#         drone["tpl_limit"] = tpl.get("tpl_limit")
#         drone["tpl_excess"] = tpl.get("tpl_excess")
#     else:
#         drone["tpl_limit"] = None
#         drone["tpl_excess"] = None
value = 10000
final_rate=6
result = value * (final_rate / 100)
print(result)
