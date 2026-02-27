import pytest
import requests

BASE_URL = "https://api.pokemonbattle.ru/v2"
AUTH_TOKEN = "сюда_вставь_свой_auth_token"  # тот что получаешь после POST /v2/auth

@pytest.fixture(scope="session")
def auth_headers():
    """Заголовки с токеном авторизации — используются во всех тестах"""
    return {"trainer_token": 'c037b656ce5d7b4cb87a26d260af5ff8'}

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture
def created_pokemon(auth_headers, base_url):
    """Создаёт покемона перед тестом и удаляет после (если нужно)"""
    response = requests.post(
        f"{base_url}/pokemons",
        headers=auth_headers,
        json={"name": "Тестовый", "photo_id": 1}
    )
    assert response.status_code == 201, f"Не удалось создать покемона: {response.text}"
    pokemon_id = response.json()["id"]
    yield pokemon_id
