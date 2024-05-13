FROM python:3.10
 
WORKDIR /app

RUN pip install poetry

COPY ./app /app

RUN poetry install
 
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]