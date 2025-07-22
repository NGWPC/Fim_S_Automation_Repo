import nbformat
from PIL import Image ,ImageChops
import base64
import io 

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


