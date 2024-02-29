from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ml/critique")
def read_item(context):
    print(context)
    return {"item_id": item_id, "q": q}

