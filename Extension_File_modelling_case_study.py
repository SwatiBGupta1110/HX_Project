#
# Starter code for Modelling Case Study Exercise
#
import json
import math

with open('parameters.json') as file:
    parameters = json.load(file)


# print(parameters)

def riebesell(x=0):
    """
    Riebesell ILF Function As given in excel spreadsheet which is as follows:

    ################################################################################################
    ' Riebesell ILF
        Function Riebesell(riebesell_base_limit As Double, riebesell_z As Double, x As Double) As Double

    Riebesell = (x / riebesell_base_limit) ^ Application.Log(1 + riebesell_z, 2)

    End
    ###############################################################################################
    """
    riebesell_base_limit = parameters["ilf_riebesell_curve"]["base_limit"]
    riebesell_z = parameters["ilf_riebesell_curve"]["z"]
    return (x / riebesell_base_limit) ** (math.log(1 + riebesell_z, 2))


def calculate_hull_values(model_data_drones, parameters):
    """
    This function calculates all values related to Hull Table which are hull_base_rate, hull_weight_adjustment,
    hull_final_rate,hull_premium
    """

    # Set Value for "hull_base_rate" from parameters
    model_data_drones = [{**drone, "hull_base_rate": parameters["base_rates_gross_in_percent"]["hull"]} for drone in
                         model_data_drones]

    # Calculate hull_weight_adjustment, hull_final_rate, hull_premium
    for drone in model_data_drones:
        drone["hull_weight_adjustment"] = parameters["adjustments_for_maximum_take_off_weight"][drone["weight"]]
        drone["hull_final_rate"] = round(drone["hull_base_rate"] * drone["hull_weight_adjustment"], 1)
        drone["hull_premium"] = round((drone["value"] * (drone["hull_final_rate"] / 100)), 1)
    return model_data_drones


def calculate_tpl_values(model_data_drones):
    """
       This function calculates all values related to TPL Table which are tpl_base_rate, tpl_base_layer_premium,
       tpl_ilf, tpl_layer_premium
       """
    # Set Value for "tpl_base_rate" from parameters
    model_data_drones = [{**drone, "tpl_base_rate": parameters["base_rates_gross_in_percent"]["liability"]} for drone
                         in model_data_drones]

    # Calculate tpl_base_layer_premium, tpl_ilf, tpl_layer_premium
    for drone in model_data_drones:
        drone["tpl_base_layer_premium"] = round((drone["value"] * (drone["tpl_base_rate"] / 100)), 1)
        drone["tpl_limit"] = 0 if drone["tpl_limit"] is None else drone["tpl_limit"]
        drone["tpl_excess"] = 0 if drone["tpl_excess"] is None else drone["tpl_excess"]
        drone["tpl_ilf"] = round(riebesell(drone["tpl_limit"] + drone["tpl_excess"]) -
                                 riebesell(drone["tpl_excess"]), 15)
        drone["tpl_layer_premium"] = round(drone["tpl_base_layer_premium"] * drone["tpl_ilf"], 1)
    return model_data_drones


def calculate_detachable_camera_values(model_data_drones, model_data_camera):
    """
           This function calculates all values related to detachable camera Table which are hull_rate,hull_premium
    """
    considered_rate = []
    for drone in model_data_drones:
        if drone["has_detachable_camera"] == True and drone["value"] > 0:
            considered_rate.append(drone["hull_final_rate"])
    # print("considered rate after filtering by given condition in spreadsheet\n", considered_rate)

    model_data_camera = [{**camera, "hull_rate": max(considered_rate)} for camera in model_data_camera]

    for camera in model_data_camera:
        camera["hull_premium"] = round((camera["value"] * (camera["hull_rate"] / 100)), 1)

    return model_data_camera


def extension1_recalculate_drone_premium(model_data_drones, max_drones_in_air, drones_dict):
    """
    This function calculates the values according to given extension 1 which is as follows:
    Customers may have a large number of drones but warrant that they will only fly a small number (n)
    at any one time. We would like to charge the full rate for the n drones with the highest calculated premiums,
    and a fixed base premium of £150 for the remaining drones.
    """
    total_drones = len(model_data_drones)
    drone_premium_acc_extension_1 = [{'serial_number': drone['serial_number'], 'hull_premium': drone['hull_premium']}
                                     for drone in model_data_drones if drone['hull_premium'] is not None]

    sorted_drones = sorted(drone_premium_acc_extension_1, key=lambda drone: drone['hull_premium'], reverse=True)

    if total_drones >= max_drones_in_air:
        sorted_drones = sorted_drones[max_drones_in_air:total_drones]

    drone_serial_numbers = [drone['serial_number'] for drone in sorted_drones]

    for serial_number in drone_serial_numbers:
        drone = drones_dict.get(serial_number)
        drone["hull_premium"] = 150

    model_data_drones = list(drones_dict.values())
    return model_data_drones


def extension2_recalculate_camera_premium(model_data_drones, model_data_camera, max_drones_in_air, camera_dict):
    """
    This function calculates the values according to given extension 2 which is as follows:

    Most of the risk of damage to cameras comes when they're in the air. If we have more cameras than drones,
    we would like to charge the full rate for the n cameras with the largest values,
    and a fixed premium of £50 for the remaining cameras.
    """
    total_camera = len(model_data_camera)
    total_drones_with_detachable_camera = len(
        list(filter(lambda drone: drone.get("has_detachable_camera") is True, model_data_drones)))

    # print("total_drones_with_detachable_camera",total_drones_with_detachable_camera)

    if total_drones_with_detachable_camera <= max_drones_in_air:
        max_camera_in_air = total_drones_with_detachable_camera
    else:
        max_camera_in_air = max_drones_in_air

    camera_premium_acc_extension_2 = [{'serial_number': camera['serial_number'], 'hull_premium': camera['hull_premium']}
                                      for camera in model_data_camera if camera['hull_premium'] is not None]

    # print("camera_premium_acc_extension_2",camera_premium_acc_extension_2)
    sorted_camera = sorted(camera_premium_acc_extension_2, key=lambda camera: camera['hull_premium'], reverse=True)
    # print("sorted_camera\n",sorted_camera)

    if total_camera >= max_camera_in_air:
        sorted_camera = sorted_camera[max_camera_in_air:total_camera]

    camera_serial_numbers = [camera['serial_number'] for camera in sorted_camera]

    for serial_number in camera_serial_numbers:
        camera = camera_dict.get(serial_number)
        camera["hull_premium"] = 50

    model_data_camera = list(camera_dict.values())
    # print("model_data_camera\n",model_data_camera)
    return model_data_camera


def calculate_net_premium(model_data_drones, model_data_camera, model_data_net_prem):
    """
    This function calculates all values related to Net Column for Premium Summary which are as follows:
    drones_hull, drones_tpl, cameras_hull, total
    """
    model_data_net_prem["drones_hull"] = sum(
        [drone["hull_premium"] for drone in model_data_drones if drone["hull_premium"] is not None])
    model_data_net_prem["drones_tpl"] = sum(
        [drone["tpl_layer_premium"] for drone in model_data_drones if drone["tpl_layer_premium"] is not None])
    model_data_net_prem["cameras_hull"] = sum(
        [camera["hull_premium"] for camera in model_data_camera if camera["hull_premium"] is not None])
    model_data_net_prem["total"] = round(sum(value for value in model_data_net_prem.values() if value is not None), 0)

    return model_data_net_prem


def calculate_gross_premium(model_data_net_prem, model_data_gross_prem, brokerage):
    """
    This function calculates all values related to Gross Column for Premium Summary which are as follows:
    drones_hull, drones_tpl, cameras_hull, total
    """
    model_data_gross_prem["drones_hull"] = (model_data_net_prem["drones_hull"] / (1 - brokerage))
    model_data_gross_prem["drones_tpl"] = (model_data_net_prem["drones_tpl"] / (1 - brokerage))
    model_data_gross_prem["cameras_hull"] = (model_data_net_prem["cameras_hull"] / (1 - brokerage))
    model_data_gross_prem["total"] = round(
        sum(value for value in model_data_gross_prem.values() if value is not None), 0)

    return model_data_gross_prem
