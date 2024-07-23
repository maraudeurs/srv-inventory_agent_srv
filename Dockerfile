ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as builder

## install pip requirements dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
        tzdata \
        gcc \
        python3-dev

COPY requirements.txt .

## Pip dependencies
ENV PYTHONDONTWRITEBYTECODE=1
ARG PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir --prefix=/usr/local --upgrade -r requirements.txt

## final image
FROM python:${PYTHON_VERSION}-slim
ARG FINAL_PYTHON_VERSION=3.11

ARG AGENT_SRV_USER="inventory_agent_clt"
ENV PATH=/root/.local/bin:$PATH
ENV TZ=Europe/Paris
## env var for python library search path
ENV LD_LIBRARY_PATH=/lib:/usr/lib:/usr/local/lib

RUN useradd -r ${AGENT_SRV_USER}

WORKDIR /app

COPY --from=builder --chmod=700 --chown=${AGENT_SRV_USER} /usr/local /usr/local
COPY --from=builder --chmod=700 --chown=${AGENT_SRV_USER} /usr/local/lib/python${FINAL_PYTHON_VERSION}/site-packages /usr/local/lib/python${FINAL_PYTHON_VERSION}/site-packages
COPY --chmod=700 --chown=${AGENT_SRV_USER} app ${WORKDIR}

USER ${AGENT_SRV_USER}

# HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

