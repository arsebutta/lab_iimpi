# Unit Testing Lab

Лабораторная работа по модульному тестированию.

## Запуск

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
pytest --cov=src --cov-report=term-missing