FROM python:3.9

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt ./app/requirements.txt
RUN pip install --no-cache-dir -r ./app/requirements.txt

COPY . /app

