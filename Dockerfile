FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /api
RUN pip3 install --upgrade pip && pip3 install poetry

COPY poetry.lock pyproject.toml /api/

RUN poetry config virtualenvs.create false &&  poetry install --no-root

COPY . /api

CMD ["uvicorn", "todo.api:bootstrap", "--host", "0.0.0.0", "--port", "800", "--factory"]
