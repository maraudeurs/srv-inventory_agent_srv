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
RUN pip install --user --no-cache-dir --upgrade -r requirements.txt

## final image
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ARG AGENT_SRV_USER="inventory_agent_clt"
ARG AGENT_SRV_GROUP=${AGENT_SRV_USER}
ENV PATH=/root/.local/bin:$PATH
ENV TZ=Europe/Paris

RUN groupadd -r ${AGENT_SRV_GROUP} && useradd -r -g ${AGENT_SRV_GROUP} ${AGENT_SRV_USER}

WORKDIR /app

COPY --chown=${AGENT_SRV_USER}:${AGENT_SRV_GROUP} --from=builder /root/.local /root/.local
COPY --chown=${AGENT_SRV_USER}:${AGENT_SRV_GROUP} --from=builder /usr/local/bin /usr/local/bin
COPY --chown=${AGENT_SRV_USER}:${AGENT_SRV_GROUP} --from=builder /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages
COPY --chown=${AGENT_SRV_USER}:${AGENT_SRV_GROUP} --chmod=700 app ${WORKDIR}

USER ${AGENT_SRV_USER}

# HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
#     CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

