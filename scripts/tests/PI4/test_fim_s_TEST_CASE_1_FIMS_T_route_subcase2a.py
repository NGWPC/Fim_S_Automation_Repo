import pytest
import os
from ..helpers import validate_directories_files
from ..utils import csv_util,compare_images_util,txt_file_validation_util

#@pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_1_FIMS_T_route_subcase2a(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,fetch_notebook_location_details,fetch_txt_details):
    tn = test_name + '.json'
    folder_name = 'PI4/data'
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         run_docker_script(folder_name,tn,scenarios,docker_command)
         print("The command ran successfully.")
    text,dir_paths = fetch_txt_details(folder_name,tn,scenarios)
    txt_file_validation_util.txt_file_validation(text,os.path.expanduser(dir_paths))
    input_notebook_location, output_notebook_location = fetch_notebook_location_details(folder_name,tn,scenarios)
    compare_images_util.image_differences(input_notebook_location,os.path.expanduser(output_notebook_location))
