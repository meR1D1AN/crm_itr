FROM ghcr.io/astral-sh/uv:0.11.2-python3.13-trixie-slim

RUN groupadd -g 1000 app_group && \
    useradd -r -u 1000 -g app_group -m -s /sbin/nologin app_user && \
    mkdir -p /app /app/staticfiles /app/media && \
    chown -R app_user:app_group /app && \
    chmod -R 775 /app /app/staticfiles /app/media

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY --chown=app_user:app_group pyproject.toml uv.lock ./

RUN uv sync --frozen && \
    uv cache prune

# Копируем остальной код проекта
COPY --chown=app_user:app_group . .

USER app_user