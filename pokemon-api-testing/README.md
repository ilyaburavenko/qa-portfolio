# 🎮 Pokemon Battle API — Testing Project

Проект по тестированию учебного REST API [pokemonbattle.ru](https://pokemonbattle.ru).  
Включает ручное тестирование (Postman), баг-репорты и автотесты на Python.

---

## 📁 Структура проекта

```
pokemon-api-testing/
├── api-testing/              # Postman-коллекция
│   └── pokemon_collection.json
├── autotests/                # Автотесты на Python (pytest + requests)
│   ├── .env.example          # Пример файла с переменными окружения
│   ├── requirements.txt
│   ├── conftest.py
│   └── tests/
│       └── test_pokemons.py
├── bug-reports/              # Баг-репорты в формате Markdown
│   ├── BUG-001.md
│   └── BUG-002.md
├── test-cases/               # Тест-кейсы
├── checklists/               # Чек-листы
└── .gitignore
```

---

## 🧪 Что протестировано

### Монолит API (`api.pokemonbattle.ru`)

| Эндпоинт | Метод | Статус |
|----------|-------|--------|
| `/v2/pokemons` | POST | ✅ |
| `/v2/pokemons` | GET (фильтры, сортировка, пагинация) | ✅ |
| `/v2/pokemons/{id}` | GET | ✅ |
| `/v2/pokemons` | PUT / PATCH | 🔄 в процессе |
| `/v2/battle` | POST | 🔄 в процессе |

---

## 🐛 Найденные баги

| ID | Эндпоинт | Описание | Severity |
|----|----------|----------|----------|
| [BUG-001](./bug-reports/BUG-001.md) | GET /v2/pokemons | Сырая ошибка pydantic при передаче строки в параметр `in_pokeball` | Minor |
| [BUG-002](./bug-reports/BUG-002.md) | GET /v2/pokemons | Сырая ошибка pydantic при передаче строки в параметр `status` | Minor |

---

## 🤖 Автотесты

Написаны на **Python + pytest + requests**.

### Запуск

**1. Клонировать репо:**
```bash
git clone https://github.com/ilyaburavenko/pokemon-api-testing.git
cd pokemon-api-testing/autotests
```

**2. Создать виртуальное окружение:**
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

**3. Установить зависимости:**
```bash
pip install -r requirements.txt
```

**4. Создать файл `.env`** на основе `.env.example`:
```
POKEMON_TOKEN=ваш_токен_здесь
```

**5. Запустить тесты:**
```bash
pytest tests/ -v
```

### Покрытие автотестами

| Класс | Тестов | Описание |
|-------|--------|----------|
| `TestCreatePokemon` | 8 | Создание покемона — позитивные, негативные, parametrize |
| `TestGetPokemons` | 10 | Список покемонов — фильтры, сортировка, пагинация, невалидные значения |
| `TestGetPokemonById` | 2 | Получение покемона по id — существующий и несуществующий |

---

## 🛠 Стек

- **Python 3.12+**
- **pytest** — фреймворк для тестов
- **requests** — HTTP-клиент
- **python-dotenv** — управление переменными окружения
- **Postman** — ручное тестирование и коллекция запросов

---

## 📋 `.env.example`

```
POKEMON_TOKEN=your_token_here
```

> Получить токен можно в [службе заботы QA Studio](https://pokemonbattle.ru).
