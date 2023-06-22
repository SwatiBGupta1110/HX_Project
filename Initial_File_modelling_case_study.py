#
# Starter code for Modelling Case Study Exercise
#
import json
import argparse

with open('parameters.json') as file:
    parameters = json.load(file)
# print(parameters)


def get_example_data():
    """
    Return an example data structure containing the inputs and placeholder outputs for the drone pricing model
    """
    example_data = {
        "insured": "Drones R Us",
        "underwriter": "Michael",
        "broker": "AON",
        "brokerage": 0.3,
        "max_drones_in_air": 2,
        "drones": [
            {
                "serial_number": "AAA-111",
                "value": 10000,
                "weight": "0 - 5kg",
                "has_detachable_camera": True,
                "tpl_limit": None,
                "tpl_excess": None,
                "hull_base_rate": None,
                "hull_weight_adjustment": None,
                "hull_final_rate": None,
                "hull_premium": None,
                "tpl_base_rate": None,
                "tpl_base_layer_premium": None,
                "tpl_ilf": None,
                "tpl_layer_premium": None
            },
            {
                "serial_number": "BBB-222",
                "value": 12000,
                "weight": "10 - 20kg",
                "has_detachable_camera": False,
                "tpl_limit": None,
                "tpl_excess": None,
                "hull_base_rate": None,
                "hull_weight_adjustment": None,
                "hull_final_rate": None,
                "hull_premium": None,
                "tpl_base_rate": None,
                "tpl_base_layer_premium": None,
                "tpl_ilf": None,
                "tpl_layer_premium": None
            },
            {
                "serial_number": "AAA-123",
                "value": 15000,
                "weight": "5 - 10kg",
                "has_detachable_camera": True,
                "tpl_limit": None,
                "tpl_excess": None,
                "hull_base_rate": None,
                "hull_weight_adjustment": None,
                "hull_final_rate": None,
                "hull_premium": None,
                "tpl_base_rate": None,
                "tpl_base_layer_premium": None,
                "tpl_ilf": None,
                "tpl_layer_premium": None
            }
        ],
        "detachable_cameras": [
            {
                "serial_number": "ZZZ-999",
                "value": 5000,
                "hull_rate": None,
                "hull_premium": None
            },
            {
                "serial_number": "YYY-888",
                "value": 2500,
                "hull_rate": None,
                "hull_premium": None
            },
            {
                "serial_number": "XXX-777",
                "value": 1500,
                "hull_rate": None,
                "hull_premium": None
            },
            {
                "serial_number": "WWW-666",
                "value": 2000,
                "hull_rate": None,
                "hull_premium": None
            }

        ],
        "gross_prem": {
            "drones_hull": None,
            "drones_tpl": None,
            "cameras_hull": None,
            "total": None
        },
        "net_prem": {
            "drones_hull": None,
            "drones_tpl": None,
            "cameras_hull": None,
            "total": None
        }
    }

    return example_data


def main(tpl_data):
    """
    Perform the rating calculations replicating 
    """
    # Your code here - replicate the spreadsheet model calculations on the data provided in model_data
    # Get the example data structure
    model_data = get_example_data()
    # print("model_data", model_data)
    # print(tpl_data)

    drones_data = model_data["drones"]

    # Getting Value for "hull_base_rate" from parameters
    drones_data= [{**d, "hull_base_rate": parameters["base_rates_gross_in_percent"]["hull"]} for d in drones_data]

    # Getting Value for "tpl_base_rate" from parameters
    drones_data= [{**d, "tpl_base_rate": parameters["base_rates_gross_in_percent"]["liability"]} for d in drones_data]
    # print("drones_data",drones_data)

    # Getting Value for "tpl_limit"  and "tpl_excess" from user passed tpl_data
    for drone in drones_data:
        for tpl in tpl_data:
            if drone["serial_number"]==tpl["serial_number"]:
                drone["tpl_limit"]=tpl["tpl_limit"]
                drone["tpl_excess"] = tpl["tpl_excess"]
    # print("drones_data", drones_data)

    # Getting "hull_weight_adjustment" for each drone
    for drone in drones_data:
        drone["hull_weight_adjustment"]=parameters["adjustments_for_maximum_take_off_weight"][drone["weight"]]

    print("drones_data", drones_data)



if __name__ == '__main__':
    # Passing tpl_limit and tpl_excess for drones
    tpl_data=[{"serial_number": "AAA-111","tpl_limit":  1000000 ,"tpl_excess": None},
              {"serial_number":"BBB-222","tpl_limit": 4000000,"tpl_excess": 1000000},
              { "serial_number": "AAA-123","tpl_limit": 5000000,"tpl_excess": 5000000}]
    main(tpl_data)

