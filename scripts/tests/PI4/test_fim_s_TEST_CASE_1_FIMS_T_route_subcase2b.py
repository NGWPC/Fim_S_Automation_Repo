
import pytest
import os
from ..helpers import validate_post_response ,validate_directories_files
from ..utils import csv_util

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_1_FIMS_T_route_subcase2b(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,run_curl_command_post,read_csv):
    tn = test_name + '.json'
    folder_name = 'PI4/data'
    # directory = fetch_directory_details(folder_name,tn,scenarios)
    # directory_util.create_directory(os.path.expanduser(directory))
#     docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
#     for docker_command in docker_commands:
#          run_docker_script(folder_name,tn,scenarios,docker_command)
#          print("The command ran successfully.")
#     url,headers,data,destination_response = run_curl_command_post(folder_name,tn,scenarios)
#     validate_post_response(url,headers,data,destination_response)
    csv_file,output_csv_file ,content_check , num_of_lines = read_csv(folder_name,tn,scenarios)
    csv_util.test_extract_csv_data(csv_file,output_csv_file,content_check ,num_of_lines)
