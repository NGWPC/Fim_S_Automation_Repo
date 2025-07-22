
import pytest
import os
from ..helpers import validate_post_response ,validate_directories_files

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_1_FIMS_T_route_subcase2b(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,run_curl_command_post):
    tn = test_name + '.json'
    folder_name = 'PI4/data'
    # directory = fetch_directory_details(folder_name,tn,scenarios)
    # directory_util.create_directory(os.path.expanduser(directory))
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         run_docker_script(folder_name,tn,scenarios,docker_command)
         print("The command ran successfully.")
    url,headers,data,destination_response = run_curl_command_post(folder_name,tn,scenarios)
    validate_post_response(url,headers,data,destination_response)
    directory_locations,directory_contents,flag = load_scenario_data(folder_name,tn,scenarios) #,flag
    validate_directories_files(directory_locations,directory_contents,flag) #,flag
