
import pytest
import os
from ..helpers import validate_directories_files

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_2_RnRApp_01_subcase3(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script):
    tn = test_name + '.json'
    folder_name = 'PI2/data'
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         run_docker_script(folder_name,tn,scenarios,docker_command)
         print("The command ran successfully.")
    directory_locations,directory_contents,flag = load_scenario_data(folder_name,tn,scenarios) #,flag
    validate_directories_files(directory_locations,directory_contents,flag) #,flag
