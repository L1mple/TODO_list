FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /api
RUN pip3 install --upgrade pip
RUN pip3 install poetry
COPY poetry.lock pyproject.toml /api/
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
COPY . /api
CMD ["celery","-A", "todo.api.main:create_api.celery_app", "worker", "-l", "info"]
