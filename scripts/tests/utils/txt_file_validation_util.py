
def txt_file_validation(text,new_file):

    with open(new_file, encoding="utf-8") as f:
        content = f.read()
    assert text in content , f"{text} not found"

