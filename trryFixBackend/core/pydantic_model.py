from pydantic import BaseModel
from typing import Optional
class URLModel(BaseModel):
    flowId: Optional[int] = 1
    name: Optional[str] = "Website Performance"
    url: Optional[str] = "https://www.tryfix.ai/"