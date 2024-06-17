ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Paris

WORKDIR /app
COPY . /app
COPY --chown=${DVB_USER} --chmod=700 * ${WORKDIR}
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
