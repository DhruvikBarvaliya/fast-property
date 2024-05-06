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
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
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
    input_file = os.path.join(current_dir, file.filename)
    output_file = os.path.join(current_dir, "test.pdf")
    print(output_file)
    # convert(file_path, pdf_file_path)
    # with open(pdf_file_path, "rb") as f:
    #     pdf_data = f.read()
    # pdf_base64 = base64.b64encode(pdf_data).decode("utf-8")
    # print(pdf_base64)
    doc = Document(input_file)

    # Create a PDF
    pdf = SimpleDocTemplate(output_file, pagesize=letter)
    styles = pdf.styles
    style = ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=12)
    styles.add(style)

    # Extract text from .docx and add to PDF
    for paragraph in doc.paragraphs:
        text = paragraph.text
        p = Paragraph(text, style)
        pdf.build([p])

    print("Conversion complete.")

    return FileResponse(output_file, filename="test.pdf", media_type="application/pdf")