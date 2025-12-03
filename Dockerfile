FROM python:3.12-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app
COPY ./main.py /code/main.py

RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
