###########
# BUILDER #
###########

# pull official base image
FROM python:3.7.6 as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY ./web/requirements/production.txt requirements.txt
RUN pip wheel --no-cache-dir --no-deps --require-hashes --wheel-dir  /usr/src/app/wheels -r requirements.txt

#########
# FINAL #
#########

# pull official base image
FROM python:3.7.6

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
#RUN addgroup -S app && adduser -S app -G app
RUN useradd app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
#RUN apt update && apt install libpq -y
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
# COPY ./entrypoint.sh $APP_HOME

# copy project
COPY ./web $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
# ENTRYPOINT ["/home/app/web/entrypoint.sh"]
