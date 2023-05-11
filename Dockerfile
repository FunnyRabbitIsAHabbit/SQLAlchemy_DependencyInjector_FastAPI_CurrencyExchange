FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim-2023-05-08

WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

ENTRYPOINT ["python", "application.py"]