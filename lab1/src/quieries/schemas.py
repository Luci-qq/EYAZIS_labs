from typing import List
import pydantic as _pydantic
from sqlalchemy import MetaData



metadata = MetaData()

class Text(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)
    name: str
    raw_text: str
    tokens: List[str] | None = None
    collocations: List[List[str]] | None = None


class CurrentTable(_pydantic.BaseModel):
    model_config = _pydantic.ConfigDict(from_attributes=True)
    name: str