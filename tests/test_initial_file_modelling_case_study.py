from Initial_File_modelling_case_study import main
import json
from Extension_File_modelling_case_study import *
import unittest
import os
import json

with open('/HX_Project/parameters.json') as file:
    parameters = json.load(file)

class MainProgramTestCase(unittest.TestCase):

    def test_calculate_premium(self):
        model_data = {
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
                    "tpl_limit": 1000000,
                    "tpl_excess": 0,
                    "hull_base_rate": 6.0,
                    "hull_weight_adjustment": 1.0,
                    "hull_final_rate": 6.0,
                    "hull_premium": 600,
                    "tpl_base_rate": 2,
                    "tpl_base_layer_premium": 200.0,
                    "tpl_ilf": 1.0,
                    "tpl_layer_premium": 200.0
                },
                {
                    "serial_number": "BBB-222",
                    "value": 12000,
                    "weight": "10 - 20kg",
                    "has_detachable_camera": False,
                    "tpl_limit": 4000000,
                    "tpl_excess": 1000000,
                    "hull_base_rate": 6.0,
                    "hull_weight_adjustment": 1.6,
                    "hull_final_rate": 9.6,
                    "hull_premium": 1152.0,
                    "tpl_base_rate": 2,
                    "tpl_base_layer_premium": 240.0,
                    "tpl_ilf":  0.527049656995122,
                    "tpl_layer_premium": 126.5
                },
                {
                    "serial_number": "AAA-123",
                    "value": 15000,
                    "weight": "5 - 10kg",
                    "has_detachable_camera": True,
                    "tpl_limit": 5000000,
                    "tpl_excess": 5000000,
                    "hull_base_rate": 6.0,
                    "hull_weight_adjustment": 1.2,
                    "hull_final_rate": 7.2,
                    "hull_premium": 1080.0,
                    "tpl_base_rate": 2,
                    "tpl_base_layer_premium": 300.0,
                    "tpl_ilf":  0.305409931399024,
                    "tpl_layer_premium": 91.6
                }
            ],
        "detachable_cameras": [
            {
                "serial_number": "ZZZ-999",
                "value": 5000,
                "hull_rate": 7.2,
                "hull_premium": 360.0
            },
            {
                "serial_number": "YYY-888",
                "value": 2500,
                "hull_rate": 7.2,
                "hull_premium": 180.0
            },
            {
                "serial_number": "XXX-777",
                "value": 1500,
                "hull_rate": 7.2,
                "hull_premium": 108.0
            },
            {
                "serial_number": "WWW-666",
                "value": 2000,
                "hull_rate": 7.2,
                "hull_premium":  144.0
            }

        ],
        "gross_prem": {
            "drones_hull": 4045.714285714286,
            "drones_tpl": 597.2857142857143,
            "cameras_hull":  1131.4285714285716,
            "total": 5774.0
        },
        "net_prem": {
            "drones_hull": 2832.0,
            "drones_tpl": 418.1,
            "cameras_hull": 792.0,
            "total": 4042.0
        }
    }

        # Call the main program or function that performs the calculations
        # and store the calculated results in a variable

        # Passing tpl_limit and tpl_excess for drones
        tpl_of_drone = [{"serial_number": "AAA-111", "tpl_limit": 1000000, "tpl_excess": None},
                        {"serial_number": "BBB-222", "tpl_limit": 4000000, "tpl_excess": 1000000},
                        {"serial_number": "AAA-123", "tpl_limit": 5000000, "tpl_excess": 5000000}]

        calculated_model_data = main(tpl_of_drone, enable_extension_1=False, enable_extension_2=False)

        # Compare the calculated results with the expected results from the provided model_data
        self.assertEqual(calculated_model_data, model_data)


if __name__ == '__main__':
    unittest.main()
