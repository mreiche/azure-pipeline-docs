FROM python:3.13-alpine

WORKDIR /home/
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

ENTRYPOINT [ "python3",  "gen.py" ]
