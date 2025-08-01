import re
def extract_name(file):
    last_line = file.strip().split('\n')[-1]
    match = re.search(r'([\w\-\.]+\.csv)',last_line)

    assert match is not None, f"csv file not found"
    csv_filename = match.group(1)
    print(csv_filename)