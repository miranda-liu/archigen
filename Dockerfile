# pull official base image
# FROM python:3.10.8-alpine as base
FROM python:3.9.13-alpine as base

# set work directory
WORKDIR /usr/src/app
RUN mkdir -p /home/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME

FROM python:3.9.13-alpine

COPY --from=base /opt/venv /opt/venv

# why are we doing this again?
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=base /usr/lib/libpq.so.5  /usr/lib/

# bug fix, need to redefine environment variables in second stage
ENV APP_HOME=/home/app/web
WORKDIR $APP_HOME

# copy entrypoint.sh
COPY ./entrypoint.sh .

RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# run entrypoint.sh
# ENTRYPOINT ["/home/app/web/entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]