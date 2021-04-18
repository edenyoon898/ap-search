FROM python:3.8-alpine

ENV FLASK_APP=./ap_search/app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev cargo
RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /ap-search
COPY . .

# docker에서 굳이 가상환경을 사용하지 않는다.
RUN pipenv lock --keep-outdated --requirements --dev > requirements.txt
RUN pip install -r ./requirements.txt

EXPOSE 5000
CMD ["flask", "run"]
