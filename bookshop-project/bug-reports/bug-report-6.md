# BUG-003: POST /review возвращает 500 при отсутствии обязательных полей

**Severity:** Major  
**Priority:** High  
**Статус:** Open

## Описание
При отправке POST /review без обязательных полей API возвращает 
500 Internal Server Error вместо 400 Bad Request или 422.

## Шаги воспроизведения
1. Отправить POST /review с телом {"author_name": "Тестировщик"}
   (без book_id, review_text, recommended)

## Ожидаемый результат
400 Bad Request или 422 с сообщением о недостающих полях

## Фактический результат
500 Internal Server Error