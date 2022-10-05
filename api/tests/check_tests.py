from fastapi import FastAPI
from fastapi.testclient import TestClient
from pprint import pprint
from .. import confidential, main, schemas
import json, os

DIR = confidential.DIR_TEST
test_check_output = {}

for i in os.listdir(DIR): 
    with open(f"tests/json_files/{i}") as outfile:
        test_check_output.update({
            f"{i}" : json.load(outfile)
        })

# pprint(test_check_output)

client = TestClient(main.app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Hello World!!!'
    assert res.status_code == 200
