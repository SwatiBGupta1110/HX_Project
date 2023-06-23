#
# Starter code for Modelling Case Study Exercise
#
import json
import math

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


"""
' Riebesell ILF
Function Riebesell(riebesell_base_limit As Double, riebesell_z As Double, x As Double) As Double

    Riebesell = (x / riebesell_base_limit) ^ Application.Log(1 + riebesell_z, 2)

End
"""
#Riebesell ILF Function
def riebesell(x=0):
    riebesell_base_limit=parameters["ilf_riebesell_curve"]["base_limit"]
    riebesell_z=parameters["ilf_riebesell_curve"]["z"]
    return (x/riebesell_base_limit)**(math.log(1 + riebesell_z, 2))

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

    considered_rate=[]
    # Getting "hull_weight_adjustment" for each drone
    for drone in drones_data:
        drone["hull_weight_adjustment"]=parameters["adjustments_for_maximum_take_off_weight"][drone["weight"]]
        drone["hull_final_rate"]=round(drone["hull_base_rate"]*drone["hull_weight_adjustment"],1)
        drone["hull_premium"]= round((drone["value"] * (drone["hull_final_rate"] / 100)),1)
        drone["tpl_base_layer_premium"] =round((drone["value"]*(drone["tpl_base_rate"]/100)),1)
        drone["tpl_excess"] = 0 if drone["tpl_excess"] is None else drone["tpl_excess"] #By using python Ternary Opeator
        drone["tpl_ilf"] = round(riebesell(drone["tpl_limit"] + drone["tpl_excess"]) - riebesell(drone["tpl_excess"]),15)
        drone["tpl_layer_premium"] = round(drone["tpl_base_layer_premium"]*drone["tpl_ilf"],1)
        if drone["has_detachable_camera"]==True and drone["value"]>0:
            considered_rate.append(drone["hull_final_rate"])
    print("drones_data", drones_data)
    print("considered rate after filtering by given condition", considered_rate)

    # Reassigning the calculated values for hull and tpl
    model_data["drones"]=drones_data

    camera_data=model_data["detachable_cameras"]

    #Getting value for "hull_rate" in detachable_cameras
    camera_data= [{**d, "hull_rate": max(considered_rate)} for d in camera_data]
    print("camera_data",camera_data)

    for d in camera_data:
        d["hull_premium"]=round((d["value"] * (d["hull_rate"] / 100)),1)
    print("camera_data", camera_data)

    model_data["detachable_cameras"]=camera_data

    #Calculating net Premium Summary
    model_data["net_prem"]["drones_hull"]=sum([d["hull_premium"] for d in drones_data ])
    model_data["net_prem"]["drones_tpl"] = sum([d["tpl_layer_premium"] for d in drones_data])
    model_data["net_prem"]["cameras_hull"] = sum([d["hull_premium"] for d in camera_data])
    model_data["net_prem"]["total"] = round(sum(int(value) for value in model_data["net_prem"].values() if value is not None),0)


    print("Here model_data",model_data)
    # Calculating gross Premium Summary
    model_data["gross_prem"]["drones_hull"] = (model_data["net_prem"]["drones_hull"]/(1-model_data["brokerage"]))
    model_data["gross_prem"]["drones_tpl"] =(model_data["net_prem"]["drones_tpl"]/(1-model_data["brokerage"]))
    model_data["gross_prem"]["cameras_hull"] =(model_data["net_prem"]["cameras_hull"]/(1-model_data["brokerage"]))
    model_data["gross_prem"]["total"] = round(sum(value for value in model_data["gross_prem"].values() if value is not None),0)
    print("Here model_data", model_data)


    drone_premium_acc_extension_1 = [{'serial_number': drone['serial_number'], 'hull_premium': drone['hull_premium']} for drone in drones_data]
    print(drone_premium_acc_extension_1)

    sorted_drones = sorted(drone_premium_acc_extension_1, key=lambda x: x['hull_premium'], reverse=True)
    total_drones = len(model_data["drones"])

    if total_drones>model_data["max_drones_in_air"]:
        for i in range(model_data["max_drones_in_air"],total_drones):
            print(sorted_drones[i])
            sorted_drones[i]["hull_premium"]=150
    print(sorted_drones)



if __name__ == '__main__':
    # Passing tpl_limit and tpl_excess for drones
    tpl_data=[{"serial_number": "AAA-111","tpl_limit":  1000000 ,"tpl_excess": None},
              {"serial_number":"BBB-222","tpl_limit": 4000000,"tpl_excess": 1000000},
              { "serial_number": "AAA-123","tpl_limit": 5000000,"tpl_excess": 5000000}]
    main(tpl_data)

