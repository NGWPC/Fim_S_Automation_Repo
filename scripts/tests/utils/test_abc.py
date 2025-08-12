import test_extract_string_from_file_util
import nbformat

file_name = test_extract_string_from_file_util.test_extract_name()

# with open("/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI6/data/extracted.txt","r") as f:
#     file_name = f.read()
def test_abc(file_name):
    print(f"This is is is {file_name}")
    notebook_path = "/home/jyoti.mikkilineni/Downloads/view_outputs(1).ipynb"
    nb = nbformat.read(notebook_path , as_version=4)
    tag_name = "update_filename"
    existing_filename = '"output_inundation_2025-06-06_14:28:32.csv"'
    updated_filename = f'"{file_name}"'

    for cell in nb.cells:
        if cell.cell_type == 'code':
            print('I am here1')
            print(cell.get("metadata", {}).get("tags", []))
            if tag_name in cell.get("metadata", {}).get("tags", []):  #'tags' in cell.metadata and tag_name in cell.metadata['tags']
                print('I am here2')
                lines = cell.source.split('\n')
                updated_lines = []
                for line in lines:
                    updated_lines.append(line.replace(existing_filename,updated_filename))
                    print('I am here')
                cell.source = '\n'.join(updated_lines)
    nbformat.write(nb,notebook_path)
    print('Updated')

test_abc(file_name)