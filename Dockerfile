FROM python:3.6.8-alpine3.6
LABEL maintainer = "Jan Piotraschke"

# Make everything fresh
# build-deps, gcc, python3-dev, musl-dev and postgresql-dev are needed for building and installing psycopg2
RUN apk update && apk upgrade && \
    apk --no-cache --update-cache add build-base gcc python3-dev musl-dev postgresql-dev freetype-dev libpng-dev openblas-dev gfortran

RUN pip install --upgrade --no-cache-dir pip
# install packages required for simulation
RUN pip install --no-cache-dir numpy python-dateutil scipy matplotlib networkx
# install panda without dependencies, otherwise it gets sad and won't install
RUN pip install --no-cache-dir --no-deps pandas
# after installing pandas, we can install seaborn
RUN pip install --no-cache-dir seaborn
# packages for web
RUN pip install --no-cache-dir psycopg2 sqlalchemy Flask Flask-WTF uuid namesgenerator pika simplejson

# wo es losgehen soll
ENTRYPOINT ["python"]

# image config
# ist nicht mein Computer, sondern wo es im Container spaeter sein wird
WORKDIR /ProjektQ/

