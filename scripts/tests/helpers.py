# tests/helpers.py

import os
import requests
import json
import logging

import requests
import nbformat
import papermill as pm

import base64
import hashlib

import pytest
from datetime import datetime, timedelta
from .utils.csv_util import wait_for_directory_existence
from deepdiff import DeepDiff



JUPYTER_URL = "http://localhost:8888"
NOTEBOOK_PATH = "notebooks/01_build_sfincs_from_nwm.ipynb"
TOKEN = ''
DOWNLOADED_NOTEBOOK_PATH = "/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI3/data/auto_notebooks/downloaded_notebook2.ipynb"

def download_notebook():
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
   
def validate_post_response(link,headers,data,destination_response_location):
    try:
      source_response = None
      destination_response = None
      response = None
      response = requests.post(link,headers=headers , data =json.dumps(data))
      try:
         response.raise_for_status()
         if response.status_code == 200:
            source_response = response.json()
            print(source_response)
         return source_response
      except requests.exceptions.HTTPError as errh:
         print(f"Bad response: {response.status_code}")
         raise errh
      except requests.exceptions.ConnectionError as errc:
         print("Conection error: " ,errc)
         raise errc 
      with open(destination_response_location, "r") as file:
         destination_response = json.load(file)
      # diff = jsondiff.diff(source_response,destination_response)
      # with open('diff_response.txt','w') as diff_file:
      #    diff_file.write(str(diff))
      assert source_response == destination_response , "source_response and destination_response rdoes not esponses match"
      logging.info("source_response and destination_response responses match")
    except AssertionError as e:
      logging.error("source_response and destination_response responses do not match")
      raise e
   
def hash_image_base64(b64):
   try:
      return hashlib.sha256(base64.b64decode(b64)).hexdigest()
   except Exception:
      return None

def clean_output(output):
   if "data" in output and "image/png" in output["data"]:
      output = output.copy()
      output["data"]["image/png"] = hash_image_base64(output["data"]["image/png"])
   return output

def normalize_outputs(outputs):
   return [clean_output(o) for o in outputs]

def compare_notebooks_using_skipped_indices(nb1_path, nb2_path , skip_indices=None):
   skip_indices = set(skip_indices or [])

   nb1 = nbformat.read(nb1_path, as_version=4)
   nb2 = nbformat.read(nb2_path, as_version=4)

   cells1 = nb1.cells
   cells2 = nb2.cells
   print(len(cells1))
   print(len(cells2))
   if len(cells1) != len(cells2) :
      print("Notebooks cells count differ")
      return False

   for i , (c1,c2) in enumerate(zip(cells1, cells2)):
      if i in skip_indices:
         print(f"Skipping {i}")
         continue
      if c1["cell_type"] != c2["cell_type"]:
         print(f"Mismatch in cell type for cell {i}")

      if c1["source"].strip() != c2["source"].strip():
         print(f"Mismatch in source  cell {i}")

      output1 = normalize_outputs(c1.get("outputs", []))
      output2 = normalize_outputs(c2.get("outputs", []))
      if i == 3:
            print(output1)
            print(output2)
      if output1 != output2 :
         print(f"Mismatch in outputs at cell {i}")
         if i == 5 :
            print(output1)
            print(output2)
         return False
   print("Notebooks match")
   return True

def fetch_generate_dynamic_files(csv_file,nc_files_base_path,csv_time_stamp,nc_time_stamp,image_file_path):
   
   dates = [datetime.today() + timedelta(days=i) for i in range(1,10)]
   start_date = datetime.today() + timedelta(days=0)
   end_date = start_date + timedelta(days=14)
   filenames = []
   for dt in dates:
     for time_str in csv_time_stamp:
      filenames.append((f"{csv_file}{dt.strftime('%Y%m%d')}{time_str}.CHRTOUT_DOMAIN1.csv","csv"))
     for time_str1 in nc_time_stamp:
      wait_for_directory_existence(nc_files_base_path,timeout = 360 , interval = 2)
      filenames.append((f"{nc_files_base_path}troute_output_{dt.strftime('%Y%m%d')}{time_str1}.nc","nc"))
   wait_for_directory_existence(image_file_path,timeout = 360 , interval = 2)
   filenames.append((f"{image_file_path}RFC_plot_output_CAGM7_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.png","png"))
   return filenames

def file_exists_and_not_empty(file_path,file_type):
   assert os.path.exists(file_path) , f"{file_type.upper()} file missing : {file_path}"
   assert os.path.getsize(file_path)>0 , f"{file_type.upper()} file is empty : {file_path}"

def compare_notebooks_using_tags(nb1_path, nb2_path , tag_name):
   nb1 = nbformat.read(nb1_path, as_version=4)
   nb2 = nbformat.read(nb2_path, as_version=4)

   tagged_cells1 = [cell for cell in nb1.cells if target_tag in cell.metadata.get("tags",[])]
   tagged_cells2 = [cell for cell in nb2.cells if target_tag in cell.metadata.get("tags",[])]

   if len(tagged_cells1) != len(tagged_cells2):
      raise AssertionError (f"Mismatch in number of tagged cells between  {tagged_cells1} and {tagged_cells2}")
   differences = []
   for i , (cell1 , cell2) in enumerate(zip(tagged_cells1,tagged_cells2)):
       nb1_tagged_cells1_output = cell1.get("outputs",[])
       nb2_tagged_cells2_output = cell2.get("outputs",[])
       variation = DeepDiff(nb1_tagged_cells1_output,nb2_tagged_cells2_output, ignore_order = True , exclude_regex_path ={"root\\[\\d+\\]\\['execution_count'\\]"})
       if variation:
         differences.append((i,variation))
         print(differences)
   if differences:
      print(differences)
      assert False , f"Not matching due to {differences}"
   else:
      print("Both the notebooks match")
       
   




   

   