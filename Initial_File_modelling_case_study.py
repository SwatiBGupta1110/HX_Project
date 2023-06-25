#
# Starter code for Modelling Case Study Exercise
#

from Extension_File_modelling_case_study import *
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


def main(tpl_of_drone,enable_extension_1=False,enable_extension_2=False):
    """
    Perform the rating calculations replicating
    """
    # Your code here - replicate the spreadsheet model calculations on the data provided in model_data

    # Get the example data structure
    model_data = get_example_data()
    # print("model data", model_data)
    # print("tpl data",tpl_data)

    # Getting Value for "tpl_base_rate" from parameters
    model_data["drones"] = [{**drone, "tpl_base_rate": parameters["base_rates_gross_in_percent"]["liability"]} for drone
                            in model_data["drones"]]

    # print('model_data["drones"] Value \n ',model_data["drones"])

    drones_dict = {drone["serial_number"]: drone for drone in model_data["drones"]}
    # print("drones_dict",drones_dict)

    # Getting Value for "tpl_limit"  and "tpl_excess" from user passed tpl_data
    for tpl in tpl_of_drone:
        drone_values = drones_dict.get(tpl["serial_number"])
        drone_values["tpl_limit"] = tpl["tpl_limit"]
        drone_values["tpl_excess"] = tpl["tpl_excess"]

    model_data["drones"] = list(drones_dict.values())
    # print("Created data structure", drones_dict)
    # print("Original data structure\n",model_data)

    # Calculating Hull Table Values hull_base_rate, hull_weight_adjustment, hull_final_rate, hull_premium
    model_data["drones"]=calculate_hull_values(model_data["drones"],parameters)
    # print('model_data["drones"]\n',model_data["drones"])

    # Calculating TPL Table Values tpl_base_rate, tpl_base_layer_premium, tpl_ilf, tpl_layer_premium
    model_data["drones"]=calculate_tpl_values(model_data["drones"])
    # print('model_data["drones"]\n',model_data["drones"])

    # Calculating hull_rate, hull_premium for detachable camera
    model_data["detachable_cameras"]=calculate_detachable_camera_values(model_data["drones"], model_data["detachable_cameras"])

    # Extension 1
    drones_dict = {drone["serial_number"]: drone for drone in model_data["drones"]}
    if enable_extension_1==True:
        model_data["drones"]=extension1_recalculate_drone_premium(model_data["drones"],
                                                                  model_data["max_drones_in_air"],
                                                                  drones_dict)

    # Extension 2
    camera_dict = {camera["serial_number"]: camera for camera in model_data["detachable_cameras"]}
    if enable_extension_2==True:
        model_data["detachable_cameras"]=extension2_recalculate_camera_premium(model_data["drones"],
                                                                               model_data["detachable_cameras"],
                                                                               model_data["max_drones_in_air"],
                                                                               camera_dict)

    # Calculating net Premium Summary
    model_data["net_prem"]=calculate_net_premium(model_data["drones"], model_data["detachable_cameras"],model_data["net_prem"])

     # Calculating gross Premium Summary
    model_data["gross_prem"]=calculate_gross_premium(model_data["net_prem"],model_data["gross_prem"],model_data["brokerage"])

    #printing Final Model Data
    print("Calculated model data: \n", model_data)

if __name__ == '__main__':
    # Passing tpl_limit and tpl_excess for drones
    tpl_of_drone=[{"serial_number": "AAA-111","tpl_limit":  1000000 ,"tpl_excess": None},
              {"serial_number":"BBB-222","tpl_limit": 4000000,"tpl_excess": 1000000},
              { "serial_number": "AAA-123","tpl_limit": 5000000,"tpl_excess": 5000000}]

    main(tpl_of_drone,enable_extension_1=False,enable_extension_2=True)
