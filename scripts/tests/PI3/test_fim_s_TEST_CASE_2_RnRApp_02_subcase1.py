
import pytest
import os
import nbformat
from ..helpers import validate_get_response,download_notebook,compare_notebooks_using_skipped_indices,compare_notebooks_using_tags
from ..utils import compare_images_util

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_2_RnRApp_02_subcase1(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,fetch_notebook_location_details):
    tn = test_name + '.json'
    folder_name = 'PI3/data'


    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         run_docker_script(folder_name,tn,scenarios,docker_command)
         print("The command ran successfully.")
    input_notebook_location, output_notebook_location = fetch_notebook_location_details(folder_name,tn,scenarios)
    for input_notebook_loc , output_notebook_loc in zip(input_notebook_location,[os.path.expanduser(each_output_notebook_location) for each_output_notebook_location in output_notebook_location]):
        compare_images_util.image_differences(input_notebook_loc,output_notebook_loc)
    for input_nb_loc , output_nb_loc in zip(input_notebook_location,[os.path.expanduser(each_output_notebook_location) for each_output_notebook_location in output_notebook_location ]):
        compare_notebooks_using_tags(input_nb_loc,output_nb_loc,"check_data")
    

    

