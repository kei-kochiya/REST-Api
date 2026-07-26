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

def test_read_single_character():
    create_response = client.post("/characters/", json={"name": "Rui", "age": 17})
    char_id = create_response.json()["id"]
    
    response = client.get(f"/characters/{char_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Rui"

def test_errors_for_missing_characters():
    get_response = client.get("/characters/999")
    assert get_response.status_code == 404
    assert get_response.json()["detail"] == "Character not found"

    delete_response = client.delete("/characters/999")
    assert delete_response.status_code == 404

def test_update_character():
    create_response = client.post("/characters/", json={"name": "Emu", "age": 15})
    char_id = create_response.json()["id"]

    update_response = client.put(
        f"/characters/{char_id}", 
        json={"name": "Emu Otori", "age": 16}
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Emu Otori"

def test_update_nonexistent_character():
    response = client.put(
        "/characters/999", 
        json={"name": "Fake", "age": 10}
    )
    assert response.status_code == 404
