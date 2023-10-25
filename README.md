# QRKot
Приложение для Благотворительного фонда поддержки котиков.

## Автор:
Алексей Наумов ( algena75@yandex.ru )
## Используемые технолологии:
* FastAPI
* SQLAlchemy
* SQLite
* Alembic
* Google Sheets API (создание отчёта по скорости сбора средств)
## Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:


```
git clone git@github.com:Algena75/QRkot_spreadsheets.git
```

```
cd QRkot_spreadsheets
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
## Как запустить проект:
```
uvicorn app.main:app --reload
```
