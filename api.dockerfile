FROM python:3.11-slim

RUN pip install --upgrade pip
RUN pip install poetry

COPY . .

RUN poetry install --no-root

ENTRYPOINT [ "poetry", "run", "python", "src/run.py" ]