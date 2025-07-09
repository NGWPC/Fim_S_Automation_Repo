
def test_txt_file_validation(text):

    with open("~/pw/automation/scripts/tests/PI5/data/output.txt", encoding="utf-8") as f:
        content = f.read()
    assert text in content , f"{target} not found"

