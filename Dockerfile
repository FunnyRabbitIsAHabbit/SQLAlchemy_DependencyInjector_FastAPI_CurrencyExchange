FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim-2023-05-08

WORKDIR /code

COPY . .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "app.application:app", "--host", "0.0.0.0", "--port", "4040"]