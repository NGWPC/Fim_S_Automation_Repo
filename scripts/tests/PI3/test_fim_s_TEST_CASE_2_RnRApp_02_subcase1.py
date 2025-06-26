
import pytest
import os
from ..helpers import validate_get_response,test_download_notebook

# @pytest.mark.skip(reason="skipping this test for now")
def test_fim_s_TEST_CASE_2_RnRApp_02_subcase1(test_name,load_scenario_data,scenarios,fetch_docker_details,run_docker_script,run_curl_command_get):
    tn = test_name + '.json'
    folder_name = 'PI3/data'
    # directory = fetch_directory_details(folder_name,tn,scenarios)
    # directory_util.create_directory(os.path.expanduser(directory))

#     docker_commands,dir_paths = fetch_docker_details(folder_name,tn,scenarios)
#     for docker_command in docker_commands:
#          run_docker_script(folder_name,tn,scenarios,docker_command)
#          print("The command ran successfully.")

#     url,headers,request_type = run_curl_command_get(folder_name,tn,scenarios)
#     out=validate_get_response(url,headers,data,request_type)
#     print(out)
test_download_notebook()
