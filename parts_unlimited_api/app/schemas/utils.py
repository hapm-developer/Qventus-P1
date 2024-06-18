from pydantic import BaseModel

class WordCount(BaseModel):
    word: str
    count: int