import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from schema import CompanyInfo
import re
load_dotenv(override=True)
google_api_key= os.getenv("GOOGLE_API_KEY")
base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
client= OpenAI(api_key= google_api_key,base_url= base_url)

def extract_company_info(text: str):
    system_prompt= """
    You are an strict information extraction system.
    Extract company information strictly in JSON format.
    Return ONLY valid JSON.
    NO markdown.
    No explanations.
    no extra text.
    return JSON in exact format:
    {
    "company_name": string,
    "industry": string,
    "pricing_model": string,
    "target_audience": string,
    "key_features": [string]
}
    """

    user_prompt=f"""
    Extract the following fields from the text:
    
    {text}
    """

    response= client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":user_prompt}
        ],
        temperature=0
        )
    
    raw_output = response.choices[0].message.content.strip()

    # Remove markdown code fences if present
    if raw_output.startswith("```"):
        raw_output = raw_output.split("```")[1]

    raw_output = raw_output.strip()

    try:
        parsed= json.loads(raw_output)
        validated= CompanyInfo(**parsed)
        return validated.model_dump()
    
    except Exception:
        repair_prompt=f"""
        The following JSON is invalid.
        Fix it and return ONLY valid JSON.
        {raw_output}
        """
        repair_response=client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role":"system","content":"You are a JSON repair system"},
                {"role":"user","content":repair_prompt}
            ],
            temperature=0
        )
        repaired = repair_response.choices[0].message.content.strip()
        repaired = re.sub(r"```json|```", "", repaired).strip()

        try:
            parsed= json.loads(repaired)
            validated= CompanyInfo(**parsed)
            return validated.model_dump()
        except Exception as e:
            return{
                "error":"Failed after retry",
                "raw_output": raw_output,
                "repaired_output":repaired
            }