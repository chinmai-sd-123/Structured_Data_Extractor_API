from pydantic import BaseModel
from typing import List

class CompanyInfo(BaseModel):
    company_name: str
    industry: str
    pricing_model: str
    target_audience: str
    key_features: List[str]