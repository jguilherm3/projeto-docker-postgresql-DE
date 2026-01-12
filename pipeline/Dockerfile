FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:least /uv /bin/

WORKDIR /code

COPY pyproject.toml .pyhton-version uv.lock ./

COPY pipeline.py .
ENTRYPOINT [ "python", "pipeline.py" ]