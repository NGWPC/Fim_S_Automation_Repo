import pytest
import os
from ..helpers import validate_directories_files
from ..utils import txt_file_validation_util

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_1_FIMS_HFSubset_subcase2(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,fetch_txt_details,remove_file):
    tn = test_name + '.json'
    folder_name = 'PI5/data'
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         print(f'Running {docker_command}')
         run_docker_script(folder_name,tn,scenarios,docker_command)
    text,dir_paths = fetch_txt_details(folder_name,tn,scenarios)
    for txt, dir_path in zip(text,[os.path.expanduser(each_dir_path_file) for each_dir_path_file in dir_paths ]):
          txt_file_validation_util.txt_file_validation(txt,dir_path)
    for dir_path in dir_paths :
         remove_file(folder_name,tn,os.path.expanduser(dir_path),scenarios)
    
