import test_extract_string_from_file_util

file_name = test_extract_string_from_file_util.test_extract_name()

# with open("/home/jyoti.mikkilineni/pw/automation/scripts/tests/PI6/data/extracted.txt","r") as f:
#     file_name = f.read()
def test_abc(file_name):
    print(f"This is is is {file_name}")

test_abc(file_name)