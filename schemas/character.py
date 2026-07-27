from pydantic import BaseModel

class CharacterCreate(BaseModel):
    name: str
    age: int

class CharacterRespond(BaseModel):
    id: int
    name: str
    age: int
