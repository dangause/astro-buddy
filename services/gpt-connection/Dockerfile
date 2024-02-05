FROM python:3.12-slim as build

ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLED_VERSION_CHECK=1 \
    PIP_NO_CHACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 
    
WORKDIR /code

EXPOSE 8000

COPY requirements/ /code/requirements

RUN set -ex \
    && apt-get update \
    && apt-get upgrade -y \
    && pip install -U pip \
    && pip install --no-cache-dir -r /code/requirements/dev.txt \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*


COPY . /code
CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--port=8000"]