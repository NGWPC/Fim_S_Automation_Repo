import pandas as pd
import os
import logging

def preprocess_df(df):
         return df.applymap(lambda x: x.strip() if isinstance(x,str) else x)

def test_extract_csv_data(csv_file,output_csv_file):
   try:
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