from fastapi import FastAPI, HTTPException
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

@app.get("/characters/", response_model = list[CharacterRespond])
def read_characters(skip: int = 0, limit: int = 10):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, age FROM characters LIMIT ? OFFSET ?",
        (limit, skip)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/characters/{char_id}", response_model = CharacterRespond)
def read_character(char_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM characters WHERE id = ?",(char_id,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return dict(row)

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

@app.put("/characters/{char_id}", response_model = CharacterRespond)
def update_character(char_id: int, character: CharacterCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE characters SET name = ?, age = ? WHERE id = ?",(character.name, character.age, char_id))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Character not found")

    conn.close()
    return {"id": char_id, "name": character.name, "age": character.age}

@app.delete("/characters/{char_id}")
def delete_character(char_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM characters WHERE id = ?",(char_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Character not found")

    conn.close()
    return {"message": "Character deleted"}