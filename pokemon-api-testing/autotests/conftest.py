import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.pokemonbattle.ru/v2"
AUTH_TOKEN = os.environ.get("POKEMON_TOKEN", "")
```

@pytest.fixture(scope="session")
def auth_headers():
    """Заголовки с токеном авторизации — используются во всех тестах"""
    return {"trainer_token": 'c037b656ce5d7b4cb87a26d260af5ff8'}

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture
def created_pokemon(auth_headers, base_url):
    response = requests.post(
        f"{base_url}/pokemons",
        headers=auth_headers,
        json={"name": "generate", "photo_id": -1}  # generate чтобы имя не повторялось
    )
    assert response.status_code == 201, f"Не удалось создать покемона: {response.text}"
    pokemon_id = response.json()["id"]
    yield pokemon_id
    # teardown — отправляем в нокаут после теста
    requests.post(
        f"{base_url}/pokemons/knockout",
        headers=auth_headers,
        json={"pokemon_id": pokemon_id}
    )