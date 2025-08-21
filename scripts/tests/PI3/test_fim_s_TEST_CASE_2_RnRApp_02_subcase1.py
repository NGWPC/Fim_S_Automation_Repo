
import pytest
import os
from ..helpers import validate_get_response,download_notebook,compare_notebooks,compare_notebooks_using_tags
from ..utils import compare_images_util

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_2_RnRApp_02_subcase1(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,fetch_notebook_location_details):
    tn = test_name + '.json'
    folder_name = 'PI3/data'
    # directory = fetch_directory_details(folder_name,tn,scenarios)
    # directory_util.create_directory(os.path.expanduser(directory))

    # docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
    # for docker_command in docker_commands:
    #      run_docker_script(folder_name,tn,scenarios,docker_command)
    #      print("The command ran successfully.")

#     url,headers,request_type = run_curl_command_get(folder_name,tn,scenarios)
#     out=validate_get_response(url,headers,data,request_type)
#     print(out)
# test_download_notebook()
# nb1_path = "/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI3/data/auto_notebooks/downloaded_notebook.ipynb"
# nb2_path = "/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI3/data/auto_notebooks/output.ipynb"
# skip_indices = []
# compare_notebooks(nb1_path,nb2_path,skip_indices)
    input_notebook_location, output_notebook_location = fetch_notebook_location_details(folder_name,tn,scenarios)
    for input_notebook_loc , output_notebook_loc in zip(input_notebook_location,[os.path.expanduser(each_output_notebook_location) for each_output_notebook_location in output_notebook_location]):
        compare_images_util.image_differences(input_notebook_loc,output_notebook_loc)
    for input_nb_loc , output_nb_loc in zip(input_notebook_location,[os.path.expanduser(each_output_notebook_location) for each_output_notebook_location in output_notebook_location ]):
        compare_notebooks_using_tags(input_nb_loc,output_nb_loc,"check_data")

