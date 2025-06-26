import requests
import nbformat
import papermill as pm


JUPYTER_URL = "http://localhost:8888"
NOTEBOOK_PATH = "notebooks/02_post_process.ipynb"
TOKEN = ''
DOWNLOADED_NOTEBOOK_PATH = "notebooks/downloaded_notebook.ipynb"

def test_download_notebook():
    api_url = f"{JUPYTER_URL}/api/contents/{NOTEBOOK_PATH}"
    headers = {"Authorization":f"Token {TOKEN}"} if TOKEN else {}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    content = response.json()['content']
    nb = nbformat.from_dict(content)
    nbformat.write(nb, DOWNLOADED_NOTEBOOK_PATH)
    print(f"Notebook at : {DOWNLOADED_NOTEBOOK_PATH}")