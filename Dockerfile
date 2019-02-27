FROM python:3.6.8-slim-stretch
LABEL maintainer = "Jan Piotraschke"

# working wir in the image
WORKDIR /ProjektQ/

# update pip
RUN pip install --upgrade --no-cache-dir pip

# install requirements
ADD requirements.txt ./
RUN pip install -r requirements.txt

# entrypoint will serve as the base for the command specified in the docker-compose.yml
ENTRYPOINT ["python"]

