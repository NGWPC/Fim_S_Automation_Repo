import pandas as pd
import os
import csv
import pytest
import random
import logging


def preprocess_df(df):
         return df.applymap(lambda x: x.strip() if isinstance(x,str) else x)

def test_extract_csv_data(csv_file,output_csv_file,content_check,num_of_lines):
   try:
     if content_check == 'self':
         random_csv_file = fetch_random_csv_file(csv_file)
         filename = os.path.basename(random_csv_file)
         csv_head = read_csv_subsetrandom_csv_file,num_of_lines)
         


     else:
      pd.set_option('display.max_columns',None)
      df_output = pd.read_csv(csv_file,sep=',', error_bad_lines=False, index_col=False, dtype='unicode') #, nrows=1
      df_output = preprocess_df(df_output)

      df_refer = pd.read_csv(output_csv_file,sep=',', error_bad_lines=False, index_col=False, dtype='unicode')#, nrows=1
      df_refer = preprocess_df(df_refer)
      
      assert os.path.exists(csv_file) == True , "Directory does not exist"
      if df_output.empty:
         print("File is empty")
      else:
         records = len(df_output)
         print("Number of records in the file:"+str(records))
      is_equal = df_output.equals(df_refer)
      # print("Both files are same: " +str(is_equal))
      logging.info(f"Both files are same: {csv_file} and {output_csv_file}")
   except pd.errors.EmptyDataError:
   #   print("CSV file is empty")
     logging.error(f"CSV file is empty: {csv_file}")
   except FileNotFounderror:
   #   print("File was not found")
     logging.error(f"File not found: {csv_file}")


def fetch_random_csv_file(dir):
   csv_files = []
   for f in os.listdir(dir):
      if f.lower().endswith('.csv') and os.path.isfile(os.path.join(dir,f)):
         csv_files.append(f)
   if not csv_files:
      raise FileNotFounderror(f"No CSV files found in {dir}")
   return os.path.join(dir, random.choice(csv_files))

def read_csv_subset(filepath,num_lines=5):
   rows = []
   with open(filepath, newline='') as csvfile:
      reader=csv.reader(csvfile)
      counter=0
      for row in reader:
         rows.append(row)
         counter+=1
         if counter>=num_lines:
            break
   return rows