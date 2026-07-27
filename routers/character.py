from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from database.models import Character
from schemas.character import CharacterCreate, CharacterRespond

router = APIRouter(
    prefix="/characters",
    tags=["Characters"]
)

@router.get("/", response_model=list[CharacterRespond])
async def read_characters(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Character).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{char_id}", response_model=CharacterRespond)
async def read_character(char_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Character).filter(Character.id == char_id))
    character = result.scalars().first()
    
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.post("/", response_model=CharacterRespond)
async def create_character(character: CharacterCreate, db: AsyncSession = Depends(get_db)):
    new_character = Character(name=character.name, age=character.age)
    
    db.add(new_character)
    await db.commit()
    await db.refresh(new_character)
    
    return new_character

@router.put("/{char_id}", response_model=CharacterRespond)
async def update_character(char_id: int, character: CharacterCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Character).filter(Character.id == char_id))
    db_character = result.scalars().first()
    
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
        
    db_character.name = character.name
    db_character.age = character.age
    await db.commit()
    await db.refresh(db_character)
    
    return db_character

@router.delete("/{char_id}")
async def delete_character(char_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Character).filter(Character.id == char_id))
    db_character = result.scalars().first()
    
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
        
    await db.delete(db_character)
    await db.commit()
    
    return {"message": "Character deleted"}
