FROM python:3.13.11-slim-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* && apt-get clean 

ADD https://astral.sh/uv/0.9.22/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-cache --locked

FROM python:3.13.11-slim-bookworm AS runtime

WORKDIR /app

COPY . .
COPY --from=builder /app/.venv ./.venv

ENV PATH="/app/.venv/bin/:$PATH"

RUN groupadd --gid 12094 non_perm_g \
 && useradd --uid 12094 --gid non_perm_g gonfreecs \
 && chown -R gonfreecs:non_perm_g .

USER gonfreecs
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

