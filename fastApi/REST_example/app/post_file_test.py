from fastapi import FastAPI, File, UploadFile
import pandas as pd
from io import StringIO

app = FastAPI()

@app.get("/")
async def say_hi():
    return {"message": "Hello World!"}

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        return {"error": "The uploaded file must be a CSV"}

    contents = await file.read()  # read file content as bytes
    df = pd.read_csv(StringIO(contents.decode('utf-8')))  # decode and parse CSV
    return {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "rows": len(df)
    }

"""
curl -X POST "http://127.0.0.1:8000/upload-csv/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@data.csv"
  
curl -X POST "http://127.0.0.1:8000/upload-csv/" \
  -F "file=@data.csv;type=text/csv"
"""