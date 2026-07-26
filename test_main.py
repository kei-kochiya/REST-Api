import pytest
import sqlite3
import os
from fastapi.testclient import TestClient
from main import app
import main

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    def get_test_db():
        conn = sqlite3.connect("test_proseka.db", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
        
    main.get_db = get_test_db
    
    conn = get_test_db()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS characters")
    cursor.execute("""
        CREATE TABLE characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
    yield
    
    if os.path.exists("test_proseka.db"):
        os.remove("test_proseka.db")

def test_create_character():
    response = client.post("/characters/", json={"name": "Ichika", "age": 16})
    assert response.status_code == 200
    assert response.json()["name"] == "Ichika"
    assert response.json()["age"] == 16
    assert "id" in response.json()

def test_read_characters():
    client.post("/characters/", json={"name": "Honami", "age": 16})
    response = client.get("/characters/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["name"] == "Honami"

def test_delete_character():
    create_response = client.post("/characters/", json={"name": "Saki", "age": 16})
    char_id = create_response.json()["id"]
    
    delete_response = client.delete(f"/characters/{char_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Character deleted"
    
    get_response = client.get("/characters/")
    assert len(get_response.json()) == 0