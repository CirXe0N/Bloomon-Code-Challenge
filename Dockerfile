FROM python:3.8

WORKDIR /usr/src/app
COPY . .

RUN mkdir ./outputs
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
