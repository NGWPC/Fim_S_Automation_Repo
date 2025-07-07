import pytest
import os
from ..helpers import validate_get_response

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_1_RnRApp_02_subcase1(test_name,load_scenario_data,scenarios,fetch_docker_details,run_R_scripts):
    tn = test_name + '.json'
    folder_name = 'PI5/data'
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         run_docker_script(folder_name,tn,scenarios,docker_command)
         print("The command ran successfully.")
