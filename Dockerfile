FROM python:3.12.6-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONFONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel "poetry==2.3.1"

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY sub-checkerBot .

RUN chmod +x prestart.sh

ENTRYPOINT ["./prestart.sh"]
CMD ["python", "main.py"]