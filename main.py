from fastapi import FastAPI
from pydantic import BaseModel
from database import init_db, get_db

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

class CharacterCreate(BaseModel):
    name: str
    age: int

class CharacterRespond(BaseModel):
    id: int
    name: str
    age: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the Proseka API! Visit /docs for the interactive API documentation."}

@app.post("/characters/", response_model = CharacterRespond)
def create_character(character: CharacterCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO characters (name, age) VALUES (?, ?)",
        (character.name, character.age)
    )
    conn.commit()
    char_id = cursor.lastrowid
    conn.close()
    return {"id": char_id, "name": character.name, "age": character.age}

@app.get("/characters/", response_model = list[CharacterRespond])
def read_characters():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM characters")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.delete("/characters/{char_id}")
def delete_character(char_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters WHERE id = ?",(char_id,))
    conn.commit()
    conn.close()
    return {"message": "Character deleted"}