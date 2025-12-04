FROM python:3.12-slim

## ----------------------------------------------------------------
## Install Packages
## ----------------------------------------------------------------
RUN apt-get update \
    && apt-get install -y gcc curl iputils-ping traceroute \
    ## cleanup
    && apt-get clean \
    && apt-get autoclean \
    && apt-get autoremove --purge  -y \
    && rm -rf /var/lib/apt/lists/*

## ----------------------------------------------------------------
## Add venv
## ----------------------------------------------------------------
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

## ----------------------------------------------------------------
## add user so we can run things as non-root
## ----------------------------------------------------------------
RUN adduser uvicornuser

## ----------------------------------------------------------------
## Set Workdir code
## ----------------------------------------------------------------
WORKDIR /code

## ----------------------------------------------------------------
## Set Python ENV
## ----------------------------------------------------------------
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/code/app:/opt/venv/bin:/opt/venv/lib/python3.12/site-packages"

## ----------------------------------------------------------------
## Copy project files for workspace
## ----------------------------------------------------------------
COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /code/app
COPY ./main.py /code/main.py

## ----------------------------------------------------------------
## Install python packages
## ----------------------------------------------------------------
RUN python3 -m pip install --upgrade pip \
 && python3 -m pip install wheel \
 && python3 -m pip install --disable-pip-version-check --no-cache-dir -r /tmp/requirements.txt

## ----------------------------------------------------------------
## Switch to non-priviliged user and run app
## the entrypoint script runs either uwisg or fastapi dev server
## ----------------------------------------------------------------
USER uvicornuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]