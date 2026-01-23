# Cifra-K Backend

REST API для управления мероприятиями, местами их проведения и погодой.  

Реализовано:

 - Импорт событий из XLSX  
 - Экспорт событий в XLSX с фильтрацией  
 - CRUD API для Event / Venue / EventImage / VenueWeather  
 - Асинхронная отправка email при публикации через Celery  
 - Swagger документация (drf‑spectacular)  
 - ERD — визуальная схема моделей  
 - Docker для локального запуска

## ERD — схема базы данных

ERD (Entity Relationship Diagram) хранится в репозитории **`diagram.png`**

---

## Локальный запуск

1. Клонировать репозиторий:

```
git clone https://github.com/doanddot/cifra-k-backend.git

cd cifra-k-backend
```

2. Запуск:

```
docker-compose up --build
```

---

## API Документация — Swagger

После старта сервера Swagger UI доступен по:

http://localhost:8000/docs

---