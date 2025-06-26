# tests/helpers.py

import os
import requests
import json
import logging

import requests
import nbformat
import papermill as pm


JUPYTER_URL = "http://localhost:8888"
NOTEBOOK_PATH = "notebooks/02_post_process.ipynb"
TOKEN = ''
DOWNLOADED_NOTEBOOK_PATH = "/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI3/data/notebooks/downloaded_notebook.ipynb"

def test_download_notebook():
    api_url = f"{JUPYTER_URL}/api/contents/{NOTEBOOK_PATH}"
    headers = {"Authorization":f"Token {TOKEN}"} if TOKEN else {}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    print(response.status_code)
    content = response.json()['content']
    nb = nbformat.from_dict(content)
    nbformat.write(nb, DOWNLOADED_NOTEBOOK_PATH)
    print(f"Notebook at : {DOWNLOADED_NOTEBOOK_PATH}")


def validate_directories_files(directory_locations, directory_contents,flag): #,flag
 
      try:
        if flag=="partly":
           for dir_location,file in zip(directory_locations,directory_contents):
            for sub_file in file:
               print(sub_file)
               file_path = os.path.join(dir_location,str(sub_file))
               assert  os.path.isfile(file_path), f"{file} is not present"
        else:
           for i,dir_location in enumerate(directory_locations):
            os.chdir(dir_location)
            assert os.getcwd() == dir_location, "Failed to load the directory" + dir_location
            dir_contents = sorted(os.listdir()) 
            print(dir_contents)    
            assert dir_contents == directory_contents[i], "Expected files not listed"
            logging.info("Expected files listed in %s", dir_location)
      except AssertionError as e:
         logging.error("Assertion failed for directory %s: %s", dir_location,e)
         raise e

def validate_get_response(link,headers,request_type):
   # try:
      source_response = None
      destination_response = None
      response = None
      response = requests.get(link,headers=headers , data =json.dumps(data))
      try:
         response.raise_for_status()
         if response.status_code == 200:
            source_response = response.json()
         return source_response
      except requests.exceptions.HTTPError as errh:
         print(f"Bad response: {response.status_code}")
         raise errh
      except requests.exceptions.ConnectionError as errc:
         print("Conection error: " ,errc)
         raise errc
      # with open(destination_response_location, "r") as file:
      #    destination_response = json.load(file)
      # diff = jsondiff.diff(source_response,destination_response)
      # with open('diff_response.txt','w') as diff_file:
      #    diff_file.write(str(diff))
      # assert source_response == destination_response , "source_response and destination_response rdoes not esponses match"
      # logging.info("source_response and destination_response responses match")
   # except AssertionError as e:
   #    logging.error("source_response and destination_response responses do not match")
   #    raise e
   
    
   


   