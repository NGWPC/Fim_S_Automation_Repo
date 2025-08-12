import test_extract_string_from_file_util
import nbformat
import re
import logging

file_name = test_extract_string_from_file_util.test_extract_name()

def update_notebook_details_util(file_name):
    logging.info(f"This is is is {file_name}")
    notebook_path = "/fsxtestautomation/data_files/fims-data/view_outputs_input_nb.ipynb"
    nb = nbformat.read(notebook_path , as_version=4)
    tag_name = "update_filename"
    existing_filename = '"output_inundation_2025-06-06_14:28:32.csv"'
    updated_filename = file_name

    for cell in nb.cells:
        if cell.cell_type == 'code':
            if tag_name in cell.get("metadata", {}).get("tags", []):
                lines = cell.source.split('\n')
                updated_lines = []
                for line in lines:
                    # This will update any existing .csv file name with the extracted file name
                    updated_line = re.sub(r'"[^"]+\.csv"',f'"{updated_filename}"',line)
                    updated_lines.append(updated_line)
                cell.source = '\n'.join(updated_lines)
    nbformat.write(nb,notebook_path)
    logging.info(f"Updated the {notebook_path}")

test_abc(file_name)