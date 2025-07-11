import pytest
import os
from ..helpers import validate_directories_files
from ..utils import gpkg_util


# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_1_FIMS_HFSubset_subcase1(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,fetch_data_file_details,remove_file):
    tn = test_name + '.json'
    folder_name = 'PI5/data'
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         print(f'Running {docker_command}')
         run_docker_script(folder_name,tn,scenarios,docker_command)
    directory_locations,directory_contents,flag = load_scenario_data(folder_name,tn,scenarios) #,flag
    validate_directories_files(directory_locations,directory_contents,flag) #,flag
    dir_path,output_file,expected_data_file,data_file_location = fetch_data_file_details(folder_name,tn,scenarios)
    gpkg_util.validate_geo_data(dir_path,output_file,os.path.expanduser(expected_data_file),os.path.expanduser(data_file_location))
    remove_file(folder_name,tn,dir_paths,scenarios)