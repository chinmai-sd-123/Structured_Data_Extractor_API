from fastapi import FastAPI, Form
from extractor import extract_company_info
from utils import fetch_website_contents

app= FastAPI()

@app.post("/extract")
async def extract(
    input_type: str= Form(...),
    text: str= Form(None),
    url: str= Form(None),
):
    if input_type== "text" and not text:
        return{"error": "please provide text"}
    
    if input_type== "url" and not url:
        return{"error": "please provide url"}
    if input_type== "url":
        content= fetch_website_contents(url)
        if content.startswith("Error:"):
            return {"error": content}
    else:
        content=text

    result= extract_company_info(content)    
    print("Extracted content preview:")
    print(content[:1000])
    return result
    
    
    