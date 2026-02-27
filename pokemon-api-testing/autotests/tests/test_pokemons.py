import pytest
import requests

BASE_URL = "https://api.pokemonbattle.ru/v2"


# ===== POST /v2/pokemons — Создание покемона =====

class TestCreatePokemon:

    def test_create_pokemon_success(self, auth_headers, base_url):
        """Позитивный: создание покемона с валидными данными"""
        response = requests.post(
            f"{base_url}/pokemons",
            headers=auth_headers,
            json={"name": "Бульбазавр", "photo_id": 1}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["message"] == "Покемон создан"
        assert "id" in data
        assert isinstance(data["id"], str)

    def test_create_pokemon_without_name(self, auth_headers, base_url):
        """Негативный: создание покемона без поля name"""
        response = requests.post(
            f"{base_url}/pokemons",
            headers=auth_headers,
            json={"photo_id": 1}
        )
        assert response.status_code == 422
        data = response.json()
        assert data["status"] == "error"

    def test_create_pokemon_without_photo_id(self, auth_headers, base_url):
        """Негативный: создание покемона без поля photo_id"""
        response = requests.post(
            f"{base_url}/pokemons",
            headers=auth_headers,
            json={"name": "Бульбазавр"}
        )
        assert response.status_code == 422
        data = response.json()
        assert data["status"] == "error"

    def test_create_pokemon_empty_name(self, auth_headers, base_url):
        """Негативный: создание покемона с пустым именем"""
        response = requests.post(
            f"{base_url}/pokemons",
            headers=auth_headers,
            json={"name": "", "photo_id": 1}
        )
        assert response.status_code == 400
        data = response.json()
        assert data["status"] == "error"
        assert data["message"] == "Имя должно содержать не менее трех символов"

    def test_create_pokemon_short_name(self, auth_headers, base_url):
        """Негативный: имя из двух символов (граничное значение)"""
        response = requests.post(
            f"{base_url}/pokemons",
            headers=auth_headers,
            json={"name": "Аб", "photo_id": 1}
        )
        assert response.status_code == 400
        data = response.json()
        assert data["message"] == "Имя должно содержать не менее трех символов"

    @pytest.mark.parametrize("name,photo_id", [
        ("Пикачу", 2),
        ("Чармандер", 3),
        ("Сквиртл", 4),
    ])
    def test_create_pokemon_various_names(self, auth_headers, base_url, name, photo_id):
        """Позитивный: создание покемонов с разными именами"""
        response = requests.post(
            f"{base_url}/pokemons",
            headers=auth_headers,
            json={"name": name, "photo_id": photo_id}
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Покемон создан"


# ===== GET /v2/pokemons — Получение списка =====

class TestGetPokemons:

    def test_get_pokemons_success(self, auth_headers, base_url):
        """Позитивный: получение списка без параметров"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_get_pokemons_in_pokeball_true(self, auth_headers, base_url):
        """Позитивный: фильтр in_pokeball=1"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"in_pokeball": 1}
        )
        assert response.status_code == 200

    def test_get_pokemons_in_pokeball_false(self, auth_headers, base_url):
        """Позитивный: фильтр in_pokeball=0"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"in_pokeball": 0}
        )
        assert response.status_code == 200

    def test_get_pokemons_status_active(self, auth_headers, base_url):
        """Позитивный: фильтр status=1 (активные)"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"status": 1}
        )
        assert response.status_code == 200

    def test_get_pokemons_status_knockout(self, auth_headers, base_url):
        """Позитивный: фильтр status=0 (в нокауте)"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"status": 0}
        )
        assert response.status_code == 200

    def test_get_pokemons_sort_asc_attack(self, auth_headers, base_url):
        """Позитивный: сортировка по возрастанию attack"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"sort": "asc_attack"}
        )
        assert response.status_code == 200

    def test_get_pokemons_sort_desc_attack(self, auth_headers, base_url):
        """Позитивный: сортировка по убыванию attack"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"sort": "desc_attack"}
        )
        assert response.status_code == 200

    def test_get_pokemons_page_large(self, auth_headers, base_url):
        """Граничный: большой номер страницы"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"page": 999}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Покемоны не найдены"

    def test_get_pokemons_invalid_in_pokeball_string(self, auth_headers, base_url):
        """Негативный (BUG-001): строка в параметре in_pokeball — ожидаем читаемую ошибку"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"in_pokeball": "абракадабра"}
        )
        assert response.status_code == 422
        data = response.json()
        assert data["status"] == "error"
        # BUG-001: сейчас возвращает сырую ошибку pydantic вместо читаемого сообщения
        # assert data["message"] == "Значение in_pokeball невалидно (1 или 0)"

    def test_get_pokemons_invalid_status_string(self, auth_headers, base_url):
        """Негативный (BUG-002): строка в параметре status — ожидаем читаемую ошибку"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"status": "абракадабра"}
        )
        assert response.status_code == 422
        data = response.json()
        assert data["status"] == "error"
        # BUG-002: сейчас возвращает сырую ошибку pydantic вместо читаемого сообщения
        # assert data["message"] == "Значение status невалидно"

    def test_get_pokemons_invalid_sort(self, auth_headers, base_url):
        """Негативный: невалидное значение sort"""
        response = requests.get(
            f"{base_url}/pokemons",
            headers=auth_headers,
            params={"sort": "абракадабра"}
        )
        assert response.status_code == 400
        data = response.json()
        assert data["message"] == "Значение sort невалидно"


# ===== GET /v2/pokemons/{id} — Получение конкретного покемона =====

class TestGetPokemonById:

    def test_get_pokemon_by_id_success(self, auth_headers, base_url, created_pokemon):
        """Позитивный: получение существующего покемона"""
        response = requests.get(
            f"{base_url}/pokemons/{created_pokemon}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data

    def test_get_pokemon_not_found(self, auth_headers, base_url):
        """Негативный: несуществующий id"""
        response = requests.get(
            f"{base_url}/pokemons/99999999",
            headers=auth_headers
        )
        assert response.status_code == 404
        data = response.json()
        assert data["status"] == "error"
        assert data["message"] == "Покемон отсутствует"
