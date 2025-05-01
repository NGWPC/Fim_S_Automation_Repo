
import pytest
import os
from ..utils import csv_util

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_2_RnRApp_01_subcase1(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,read_csv):
    tn = test_name + '.json'
    folder_name = 'PI2/data'
    # directory = fetch_directory_details(folder_name,tn,scenarios)
    # directory_util.create_directory(os.path.expanduser(directory))
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         run_docker_script(folder_name,tn,scenarios,docker_command)
         print("The command ran successfully.")
    csv_file,output_csv_file = read_csv(folder_name,tn,scenarios)
    csv_util.test_extract_csv_data(os.path.expanduser(csv_file),os.path.expanduser(output_csv_file))
