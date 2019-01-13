FROM python:3.6.8-alpine3.6
LABEL maintainer = "Jan Piotraschke"

# Make everything fresh
# build-deps, gcc, python3-dev, musl-dev and postgresql-dev are needed for building and installing psycopg2
# 
RUN apk update && apk upgrade && \
    apk add --virtual build-deps gcc gfortran python3-dev musl-dev && \
    apk add postgresql-dev freetype-dev libpng-dev openblas-dev

# pip
# Version mit angeben; kann man nicht in requirements.txt
RUN pip install 'psycopg2==2.7.3.2' 'numpy' 'pandas' 'matplotlib' 'seaborn' 'scipy' 'sqlalchemy'

# wo es losgehen soll
ENTRYPOINT python /ProjektQ/SDTM.py

# image config
# ist nicht mein Computer, sondern wo es im Container spaeter sein wird
WORKDIR /ProjektQ/
EXPOSE 80
