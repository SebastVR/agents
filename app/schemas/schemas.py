from typing import List

from pydantic import BaseModel


class TOCEntry(BaseModel):
    level: int
    text: str
    page: int = 0
