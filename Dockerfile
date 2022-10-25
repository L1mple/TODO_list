FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install poetry
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY . /app
