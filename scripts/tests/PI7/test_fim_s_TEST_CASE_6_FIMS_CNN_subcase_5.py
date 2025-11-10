import pytest
import os
from ..helpers import validate_directories_files,fetch_latest_file,file_exists_and_not_empty
from ..utils import csv_util,compare_images_util,txt_file_validation_util

#@pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_6_FIMS_CNN_subcase_5(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,fetch_notebook_location_details,fetch_txt_details,remove_file):
    tn = test_name + '.json'
    folder_name = 'PI7/data'
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         run_docker_script(folder_name,tn,scenarios,docker_command)
         print("The command ran successfully.")
    file = fetch_latest_file(dir_paths)
    print(file)
    file_exists_and_not_empty(file,"tif")
    remove_file(folder_name,tn,file,scenarios)