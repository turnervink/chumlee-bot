# https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

# user a builder image to reduce the size of the final image
FROM python:3.12-bullseye AS builder

# pin the version of poetry to reduce the risk of breaking changes
RUN pip install poetry===1.8.3

# POETRY_NO_INTERACTION=1 prevents poetry from asking for user input
# create the virtualenv in the project to keep dependencies isolated
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# install dependencies, add --without to skip dev dependencies if needed
# remove the cache to reduce the size of the final image
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

FROM python:3.12-slim-bullseye AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src

CMD ["python", "-u", "src/bot.py"]