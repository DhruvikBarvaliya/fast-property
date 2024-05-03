from typing import Union
from fastapi import FastAPI

app = FastAPI()
from docx2pdf import convert

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items")
async def read_item(input_data: dict):
    print(input_data,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    input_file = input_data.get("num1")

    output_file = input_data.get("num2")
    convert(input_file, output_file)

    return {"item_id": "ok"}
