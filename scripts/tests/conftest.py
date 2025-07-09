# tests/conftest.py

import pytest
import os
import subprocess
import logging 
import json
import requests

#Logging code
### Adding Logger logic ##########
logging.basicConfig(level=logging.INFO,

  format = '%(asctime)s - %(levelname)s -%(message)s')

@pytest.fixture(scope="session")
def scenarios():
    def _scenarios(folder_name,data_file):
         with open(os.path.join(os.path.dirname(__file__), folder_name,data_file), 'r') as file:
          return json.load(file)
    return _scenarios

@pytest.fixture
def run_shell_script():
    def _run_shell_script(folder_name,data_file, scenarios):
        scenario = scenarios(folder_name , data_file)
    # print("Display param here " +request.param)
        shell_script = scenario['additional_data'][0].get('shell_script')
        result =  subprocess.run(['bash',os.path.expanduser(shell_script)],stdout = subprocess.PIPE , universal_newlines = True)
        variable_value = result.stdout.strip()
        dir_path = scenario['additional_data'][0].get('base_directory')+ variable_value.split('\n',1)[0]
        return os.path.expanduser(dir_path),scenario['additional_data'][0].get('output_file'),scenario['additional_data'][0].get('expected_data_file'),scenario['additional_data'][0].get('data_file_location')

    return _run_shell_script

@pytest.fixture
def run_shell_script_from_directory():
    def _run_shell_script_from_directory(folder_name,data_file, scenarios):
     try:
        scenario = scenarios(folder_name , data_file)
        shell_script = scenario['additional_data'][0].get('shell_script')
        location = scenario['additional_data'][0].get('base_directory')
        result = subprocess.run(f"cd {location} && sudo bash {shell_script}",shell=True,check=True,stdout = subprocess.PIPE,stderr = subprocess.PIPE,universal_newlines = True)
        print("Output:",result.stdout)
     except subprocess.CalledProcessError as e:
        print("Error:",e.stderr)
        raise e
    return _run_shell_script_from_directory   

@pytest.fixture
def run_R_Scripts():
    def _run_R_scripts(folder_name,data_file, scenarios,command):
        try:
            result =  subprocess.run(command,stdout = subprocess.PIPE , stderr = subprocess.PIPE , universal_newlines = True , shell = True , check = True, executable ="/usr/bin/bash")
            print(result.stdout.strip())
            print(result.stderr)     
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Docker command failed : {e}")
            print(result.stderr)
            raise e
    return _run_R_scripts 

@pytest.fixture
def change_dir(run_shell_script):
    dir_path , _  = run_shell_script
    os.chdir(dir_path)
    yield
    os.chdir(os.path.dirname(dir_path))

@pytest.fixture
def load_scenario_data():
    def _load_scenario_data(folder_name,scenario_name,scenarios):
            data = scenarios(folder_name , scenario_name)
            directory_locations = data['d_loc']
            directory_contents = data['d_files']
            flag = data['additional_data'][0].get("flag")
            return directory_locations,directory_contents,flag
    return _load_scenario_data

@pytest.fixture
def test_name(request):
    print(f"Running test: {request.node.name}")
    return request.node.name

@pytest.fixture
def remove_file():
    def _remove_file(folder_name , data_file , file_name_path,scenarios):
      assert os.path.exists(file_name_path)
      scenario = scenarios(folder_name , data_file)
      shell_script = scenario['additional_data'][0].get('remove_file_shell_script')
      result = subprocess.run(['bash',os.path.expanduser(shell_script) ,file_name_path ],stdout = subprocess.PIPE, universal_newlines = True)
      print("File to be removed: "+result.stdout.strip())
      return result.stdout.strip()
    return _remove_file   

@pytest.fixture
def remove_directory():
    def _remove_directory(folder_name , data_file , file_name_path,scenarios):
      assert os.path.exists(file_name_path)
      scenario = scenarios(folder_name , data_file)
      shell_script = scenario['additional_data'][0].get('remove_directory_shell_script')
      result = subprocess.run(['bash',os.path.expanduser(shell_script) ,file_name_path ],stdout = subprocess.PIPE, universal_newlines = True)
      print("File to be removed: "+result.stdout.strip())
      return result.stdout.strip()
    return _remove_directory

@pytest.fixture
def read_csv():
    def _read_csv(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('csv_file') , scenario['additional_data'][0].get('output_csv_file'), scenario['additional_data'][0].get('content_check'), scenario['additional_data'][0].get('number_of_lines')
    return _read_csv 

@pytest.fixture
def fetch_data_file_details():
    def _fetch_data_file_details(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('base_directory') , scenario['additional_data'][0].get('output_file'), scenario['additional_data'][0].get('expected_data_file'),scenario['additional_data'][0].get('data_file_location')
    return _fetch_data_file_details 

@pytest.fixture
def fetch_data_file_metadata_details():
    def _fetch_data_file_metadata_details(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('source_file'), scenario['additional_data'][0].get('expected_data_file'),scenario['additional_data'][0].get('fields')
    return _fetch_data_file_metadata_details 
        
@pytest.fixture
def read_txt():
    def _read_txt(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('text_file_location'),scenario['additional_data'][0].get('total_records'),scenario['additional_data'][0].get('expected_record_value')
    return _read_txt 

@pytest.fixture
def read_me():
    def _read_me(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('source_read_me_location'),scenario['additional_data'][0].get('destination_read_me_location')
    return _read_me 

@pytest.fixture
def json_read():
    def _json_read(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('source_json_file_location'),scenario['additional_data'][0].get('destination_json_file_location')
    return _json_read 

@pytest.fixture
def read_vrt():
    def _read_vrt(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('source_vrt_file_location'),scenario['additional_data'][0].get('destination_vrt_file_location'),scenario['additional_data'][0].get('remove_files')
    return _read_vrt 

@pytest.fixture
def read_tif():
    def _read_tif(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('source_tif_file_location'),scenario['additional_data'][0].get('destination_tif_file_location')
    return _read_tif

@pytest.fixture
def fetch_docker_details():
    def _fetch_docker_details(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('docker_commands'),scenario['additional_data'][0].get('remove_files')
    return _fetch_docker_details


@pytest.fixture
def run_docker_script():
    def _run_docker_script(folder_name,data_file, scenarios,docker_command):
        try:
            result =  subprocess.run(docker_command,stdout = subprocess.PIPE , stderr = subprocess.PIPE , universal_newlines = True , check = True , shell = True , executable ="/usr/bin/bash")
            print(result.stdout.strip())
            print(result.stderr)   
            print('I am here')  
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Docker command failed : {e}")
            print(result.stderr)
            raise e
    return _run_docker_script

@pytest.fixture
def sql_read():
    def _sql_read(folder_name , data_file, scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('base_directory')
    return _sql_read


@pytest.fixture
def fetch_directory_details():
    def _fetch_directory_details(folder_name,data_file,scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('directory')
    return _fetch_directory_details


@pytest.fixture
def run_curl_command_post():
    def _run_curl_command_post(folder_name,data_file,scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('url') , scenario['additional_data'][0].get('headers') , scenario['additional_data'][0].get('data'),scenario['additional_data'][0].get('destination_response_location')
    return _run_curl_command_post

@pytest.fixture
def run_curl_command_get():
    def _run_curl_command_get(folder_name,data_file,scenarios):
         scenario = scenarios(folder_name , data_file)
         return scenario['additional_data'][0].get('url') , scenario['additional_data'][0].get('headers') , scenario['additional_data'][0].get('request_type')
    return _run_curl_command_get

@pytest.fixture
def env_file_check():
    def _env_file_check(folder_name,data_file,scenarios):
        scenario = scenarios(folder_name , data_file)
        return scenario['additional_data']
    return _env_file_check


@pytest.fixture
def env_file_check():
    def _env_file_check(folder_name,data_file,scenarios):
        scenario = scenarios(folder_name , data_file)
        return scenario['additional_data']
    return _env_file_check


@pytest.fixture
def fetch_stac_ui_details():
    def _fetch_stac_ui_details(folder_name,data_file,scenarios):
        scenario = scenarios(folder_name , data_file)
        return scenario['additional_data'][0].get("link") , scenario['additional_data'][0].get("item")
    return _fetch_stac_ui_details
