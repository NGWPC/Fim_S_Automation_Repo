import nbformat
from PIL import Image ,ImageChops
import base64
import io 
import logging
from bs4 import BeautifulSoup

def verify_gdf_output(path, tag_name = 'compare_image'):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
    images=[]
    tagged_cells_exist = False
    for cell in nb.cells:
        if cell.cell_type == "code" and tag_name in cell.get("metadata", {}).get("tags", []):
            tagged_cells_exist = True
            outputs = cell.get("outputs", [])
            for output in outputs:
                if output.output_type in ("display_data", "execute_result"):
                    img_details = output.data.get("text/html")
                    if img_details:
                        logging.info("Interactive map exists")

    assert tagged_cells_exist , f"No tagged cell exist for {path}"
    assert img_details, f"Tagged cells exist but no interactive maps  were found in {path}"

def extract_images(path, tag_name = 'compare_image'):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
    images=[]
    tagged_cells_exist = False
    for cell in nb.cells:
        if cell.cell_type == "code" and tag_name in cell.get("metadata", {}).get("tags", []):
            tagged_cells_exist = True
            outputs = cell.get("outputs", [])
            for output in outputs:
                if output.output_type in ("display_data", "execute_result"):
                    img_details = output.data.get("image/png")
                    if img_details:
                        img = Image.open(io.BytesIO(base64.b64decode(img_details)))                      
                        images.append(img)

    assert tagged_cells_exist , f"No tagged cell exist for {path}"
    assert images, f"Tagged cells exist but no images were found in {path}"
    return images

def compare_images(img1,img2):
    diff = ImageChops.difference(img1,img2)
    return diff.getbbox() is None


def image_differences(input_notebook_location,output_notebook_location):
    output_image1 = extract_images(output_notebook_location) 
    output_image2 = extract_images(input_notebook_location)   

    for i, (img1,img2) in enumerate(zip(output_image1, output_image2)):
        is_same = compare_images(img1,img2)
        if is_same:
            print(f"plot {i}:Match")
        else:
            diff = diff = ImageChops.difference(img1,img2)
            img_diff_path = f"diff_plot_{i}.png"
            diff.save(img_diff_path)
            assert False , f"Plot {i} differs" 

# def list_cells(notebook_path):
    
#     with open(notebook_path , 'r' , encoding='utf-8') as f:
#         nb = nbformat.read(f , as_version=4)
    
#     for i, cell in enumerate(nb.cells):
#         cell_type = cell.cell_type
#         tags = cell.metadata.get("tags",[])
#         has_output = bool(cell.get("outputs"))
#         print(f"Index: {i} | Type: {cell_type} | Tags:{tags} | Has Output: {has_output}")

# list_cells("/fsxtestautomation/data_files/fims-data/run_v22.ipynb")

def verify_table_fields(path, tag_name = 'table_validation'):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
    expected_fields = {'field_1','feature_id','feature_id_str','strm_order','name','state','streamflow_cfs','inherited_rfc_forecasts','max_status','reference_time','update_time','geometry'}
    tagged_cells_exist = False
    for cell in nb.cells:
        if cell.cell_type == "code" and tag_name in cell.get("metadata", {}).get("tags", []):
            tagged_cells_exist = True
            outputs = cell.get("outputs", [])
            for output in outputs:
                if output.output_type in ("display_data", "execute_result"):
                    columns = output.data.get("text/html")
                    if columns:
                        soup = BeautifulSoup(columns, "html.parser")
                        table = soup.find("table")
                        if table:
                            headers = {th.get_text(strip=True) for th in table.find_all("th")}
                            if expected_fields.issubset(headers):
                                logging.info(f"All expected columns {expected_fields} found")
                                return True
                            else:
                                missing = expected_fields - headers
                                logging.info(f"Missing fields : {missing}")
                                assert False, f"Missing columns {missing}"
                                
                        else:
                            logging.info("Table missing")
                            assert False, f"Missing table"
        else:
            assert False , f"Required data not available"
    assert tagged_cells_exist , f"No tagged cell exist for {path}"
   


