import re
def test_extract_name():
    with open('/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI6/data/post_process_output.txt','r') as f :
        out = f.read()
    # file = '/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI6/data/post_process_output.txt'
    last_line = out.strip().split('\n')[-1]
    match = re.search(r'([\w\-:\.]+\.csv)',last_line)
    # assert match is not None, f"csv file not found"
    # csv_filename = match.group(0)
    # print( "I am here")
    # print(csv_filename)
    if match:
        file_name = match.group(1)
        return file_name
    else :
        raise ValueError(f"No csv filname found in {last_line}")

# if __name__ == "__main__":
#     file_name = test_extract_name()
#     print(file_name)