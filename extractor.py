import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from schema import CompanyInfo

load_dotenv(override=True)
google_api_key= os.getenv("GOOGLE_API_KEY")
base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
client= OpenAI(api_key= google_api_key,base_url= base_url)

def extract_company_info(text: str):
    system_prompt= """
    You are an information extraction system.
    Extract company information strictly in JSON format.
    Return ONLY valid JSON.
    NO markdown.
    No explanations.
    no extra text.
    """

    user_prompt="""
    Extract the following fields from the text:
    -company_name
    -industry
    -pricing_model
    -target_audience
    -key_features (list)

    Text: {text}
    """

    response= client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ],
        temperature=0
        )
    
    raw_output= response.choices[0].message.content

    return raw_output