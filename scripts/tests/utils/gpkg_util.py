import geopandas
import logging
import os

def compare_gpkgs(source_file,destination_file):
    print(source_file)
    source_gdf = geopandas.read_file(source_file)
    destination_gdf = geopandas.read_file(destination_file)

    try:
        assert source_gdf.equals(destination_gdf),"Dataframes not equal"
        logging.info(f"Both gpkg files are same: {source_file} and {destination_file}")
    except AssertionError as e:
        # print(f"\n {str(e)} \n")
        logging.error(f"Both gpkg files are not same: {source_file} and {destination_file}")
        raise e


def validate_geo_data(dir_path,output_file,expected_data_file,data_file_location):
   try:
      assert os.path.isdir(dir_path) == True , "Directory1 does not exist"+dir_path
      assert os.path.exists(dir_path) == True , "Directory does not exist"+dir_path

      # print(f"current working directory: {os.getcwd()}")

      dir_contents = sorted(os.listdir())
      file_path = os.path.join(dir_path,output_file)
      assert os.path.isfile(file_path) == True , "File does not exist"
   
      # qgis_util.test_run(dir_path, output_file,expected_data_file)
      compare_gpkgs(file_path,data_file_location)
   except AssertionError as e:
      logging.error("Assertion failed for directory %s: %s",file_path,e)
      raise e