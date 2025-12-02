import pytest
import os
from ..helpers import validate_directories_files,fetch_latest_file,file_exists_and_not_empty
from ..utils import compare_images_util

#@pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_6_FIMS_CNN_subcase_4(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,fetch_notebook_location_details,fetch_txt_details,run_shell_script_from_directory,remove_file):
    tn = test_name + '.json'
    folder_name = 'PI7/data'
    docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    for docker_command in docker_commands:
         run_docker_script(folder_name,tn,scenarios,docker_command)
         print("The command ran successfully.")
    input_notebook_location, output_notebook_location = fetch_notebook_location_details(folder_name,tn,scenarios)
    compare_images_util.image_differences(input_notebook_location,os.path.expanduser(output_notebook_location))
    # compare_images_util.verify_table_fields(os.path.expanduser(output_notebook_location),tag_name = 'table_validation')