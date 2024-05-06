# from typing import Union
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.post("/items")
# async def read_item(input_data: dict):
#     print(input_data,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
#     input_file = input_data.get("docxPath")

#     output_file = input_data.get("filePath")
#     convert(input_file, output_file)

#     return {"item_id": "ok"}


# from fastapi import FastAPI, UploadFile, File

# app = FastAPI()
# import os
# from docx2pdf import convert

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# current_dir = os.path.dirname(__file__)
# pdf_file_path = os.path.join(current_dir,"test.pdf")
# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     contents = await file.read()
#     with open(f"{file.filename}", "wb") as f:
#         f.write(contents)
#     file_path = os.path.join(current_dir,file.filename)
#     convert(file_path, pdf_file_path)
#     with open(pdf_file_path, "rb") as f:
#         converted_file = f.read()
#     return {"filename": file.filename, "convert_file" : converted_file}


from fastapi import FastAPI, UploadFile, File
import os
# from docx2pdf import convert
from fastapi.responses import Response, FileResponse
app = FastAPI()
import base64

current_dir = os.path.dirname(__file__)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    with open(f"{file.filename}", "wb") as f:  # Use "wb" mode for writing binary data
        f.write(contents)
    file_path = os.path.join(current_dir, file.filename)
    pdf_file_path = os.path.join(current_dir, "test.pdf")
    print(pdf_file_path)
    # convert(file_path, pdf_file_path)
    # with open(pdf_file_path, "rb") as f:
    #     pdf_data = f.read()
    # pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
    # print(pdf_base64)
    from docx import Document
    from subprocess import Popen, PIPE
    doc = Document(file_path)
    # Save the DOCX file as HTML
    html_file = file_path.replace('.docx', '.html')
    doc.save(html_file)
    # Convert HTML to PDF using libreoffice
    libreoffice_cmd = ['libreoffice', '--headless', '--convert-to', 'pdf', html_file, '--outdir', os.path.dirname(pdf_file_path)]
    libreoffice_process = Popen(libreoffice_cmd, stdout=PIPE, stderr=PIPE)
    libreoffice_process.communicate()
    # Remove the temporary HTML file
    os.remove(html_file)
    print(f"Conversion completed. PDF saved as {pdf_file_path}")

    return FileResponse(pdf_file_path, filename="test.pdf", media_type="application/pdf")