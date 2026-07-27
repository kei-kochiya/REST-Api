import sqlite3
from fastapi import APIRouter, HTTPException, Depends

from database.connection import get_db
from schemas.character import CharacterCreate, CharacterRespond

router = APIRouter(
    prefix = "/characters",
    tags = ["Characters"]
)

@router.get("/", response_model = list[CharacterRespond])
def read_characters(skip: int = 0, limit: int = 10, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, name, age FROM characters LIMIT ? OFFSET ?",
        (limit, skip)
    )
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

@router.get("/{char_id}", response_model = CharacterRespond)
def read_character(char_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name, age FROM characters WHERE id = ?",(char_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return dict(row)

@router.post("/", response_model = CharacterRespond)
def create_character(character: CharacterCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO characters (name, age) VALUES (?, ?)",
        (character.name, character.age)
    )
    db.commit()
    char_id = cursor.lastrowid
    return {"id": char_id, "name": character.name, "age": character.age}

@router.put("/{char_id}", response_model = CharacterRespond)
def update_character(char_id: int, character: CharacterCreate, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE characters SET name = ?, age = ? WHERE id = ?",(character.name, character.age, char_id))
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Character not found")

    return {"id": char_id, "name": character.name, "age": character.age}

@router.delete("/{char_id}")
def delete_character(char_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM characters WHERE id = ?",(char_id,))
    db.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Character not found")

    return {"message": "Character deleted"}