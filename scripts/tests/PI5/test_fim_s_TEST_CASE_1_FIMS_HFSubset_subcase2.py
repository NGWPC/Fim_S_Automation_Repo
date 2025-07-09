import pytest
import os
from ..helpers import validate_directories_files

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_1_FIMS_HFSubset_subcase2(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,remove_file):
    tn = test_name + '.json'
    folder_name = 'PI5/data'
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         print(f'Running {docker_command}')
         run_docker_script(folder_name,tn,scenarios,docker_command)
