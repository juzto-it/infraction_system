FROM python:3.8.8
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code

RUN pip install --upgrade pip
RUN apt-get update && apt-get -y install ghostscript
RUN pip install -r ./requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
