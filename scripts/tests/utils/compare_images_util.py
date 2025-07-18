import nbformat
from PIL import Image ,ImageChops
import base64
import io 

def extract_images(path, tag_name = 'compare_image'):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)
    images=[]
    for cell in nb.cells:
        if cell.cell_type == "code" and tag_name in cell.get("metadata", {}).get("tags", []):
            outputs = cell.get("outputs", [])
            for output in outputs:
                if output.output_type in ("display_data", "execute_result"):
                    img_details = output.data.get("image/png")
                    if img_details:
                        img = Image.open(io.BytesIO(base64.b64decode(img_details)))
                        images.append(img)
    return images

def compare_images(img1,img2):
    diff = ImageChops.difference(img1,img2)
    return diff.getbbox() is None

output_image1 = extract_images("/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI4/data/output.ipynb") 
output_image2 = extract_images("/home/jyoti.mikkilineni/Downloads/run_v22(1).ipynb")   

for i, (img1,img2) in enumerate(zip(output_image1, output_image2)):
    is_same = compare_images(img1,img2)
    print(f"plot {i}:{'Match' if is_same else 'Different'}")
# def list_cells(notebook_path):
    
#     with open(notebook_path , 'r' , encoding='utf-8') as f:
#         nb = nbformat.read(f , as_version=4)
    
#     for i, cell in enumerate(nb.cells):
#         cell_type = cell.cell_type
#         tags = cell.metadata.get("tags",[])
#         has_output = bool(cell.get("outputs"))
#         print(f"Index: {i} | Type: {cell_type} | Tags:{tags} | Has Output: {has_output}")

# list_cells("/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI4/data/run_v22_executed.ipynb")


