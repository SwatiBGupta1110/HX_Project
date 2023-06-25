import unittest
from unittest.mock import patch
from io import StringIO
from Extension_File_modelling_case_study import *


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


class ModellingCaseStudyTestCase(unittest.TestCase):

    def setUp(self):
        # Create a test data structure
        self.test_data = {
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

        # Patch the 'open' function to return the test data
        self.mock_open = patch('__main__.open', create=True)
        self.mock_file = self.mock_open.start()
        self.mock_file.return_value.__enter__.return_value = StringIO(json.dumps(self.test_data))

    def tearDown(self):
        # Stop patching the 'open' function
        self.mock_open.stop()

    def test_get_example_data(self):
        # Test the 'get_example_data' function
        example_data = get_example_data()
        self.assertEqual(example_data, self.test_data)

    def test_calculate_hull_values(self):
        # Test the 'calculate_hull_values' function
        drones = self.test_data["drones"]
        calculated_drones = calculate_hull_values(drones, parameters)

        # Add assertions to check the calculated values
        for drone in calculated_drones:
            assert "hull_base_rate" in drone
            assert "hull_weight_adjustment" in drone
            assert "hull_final_rate" in drone
            assert "hull_premium" in drone

            # Additional assertions for specific calculations
            assert isinstance(drone["hull_base_rate"], float)
            assert isinstance(drone["hull_weight_adjustment"], float)
            assert isinstance(drone["hull_final_rate"], float)
            assert isinstance(drone["hull_premium"], float)

    def test_calculate_tpl_values(self):
        # Test the 'calculate_tpl_values' function
        drones = self.test_data["drones"]
        calculated_drones = calculate_tpl_values(drones)

        # Add assertions to check the calculated values
        for drone in calculated_drones:
            assert "tpl_base_rate" in drone
            assert "tpl_base_layer_premium" in drone
            assert "tpl_ilf" in drone
            assert "tpl_layer_premium" in drone

            # Additional assertions for specific calculations
            assert isinstance(drone["tpl_base_rate"], float)
            assert isinstance(drone["tpl_base_layer_premium"], float)
            assert isinstance(drone["tpl_ilf"], float)
            assert isinstance(drone["tpl_layer_premium"], float)

    def test_extension1_recalculate_drone_premium(self):
        # Test the 'extension1_recalculate_drone_premium' function
        model_data_drones = self.test_data["drones"]
        max_drones_in_air = 3
        drones_dict = {drone["serial_number"]: drone for drone in model_data_drones}

        recalculated_drones = extension1_recalculate_drone_premium(model_data_drones, max_drones_in_air, drones_dict)

        # Add assertions to check the recalculated drone premiums
        for drone in recalculated_drones:
            if drone["serial_number"] in drones_dict:
                assert drone["hull_premium"] == drones_dict[drone["serial_number"]]["hull_premium"]
            else:
                assert drone["hull_premium"] == 150

        # Additional assertions for the modified drones
        assert len(recalculated_drones) == len(model_data_drones)

    def test_extension2_recalculate_camera_premium(self):
        # Test the 'extension2_recalculate_camera_premium' function
        model_data_drones = self.test_data["drones"]
        model_data_camera = self.test_data["detachable_cameras"]
        max_drones_in_air = 3
        camera_dict = {camera["serial_number"]: camera for camera in model_data_camera}

        recalculated_cameras = extension2_recalculate_camera_premium(
            model_data_drones, model_data_camera, max_drones_in_air, camera_dict)

        # Add assertions to check the recalculated camera premiums
        for camera in recalculated_cameras:
            if camera["serial_number"] in camera_dict:
                assert camera["hull_premium"] == camera_dict[camera["serial_number"]]["hull_premium"]
            else:
                assert camera["hull_premium"] == 50

        # Additional assertions for the modified cameras
        assert len(recalculated_cameras) == len(model_data_camera)


if __name__ == '__main__':
    unittest.main()
