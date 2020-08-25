FROM python:3.8.3-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt

RUN apt-get update && \
    apt-get install -y wget netcat && \
    wget -q https://raw.githubusercontent.com/eficode/wait-for/master/wait-for -P /usr/local/bin && \
    chmod +x /usr/local/bin/wait-for && \
    pip install --upgrade pip

RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

RUN chmod +x /usr/src/app/app/start.sh

CMD ["/usr/src/app/app/start.sh"]
