FROM python:3.6.8-slim-stretch
LABEL maintainer = "Jan Piotraschke"

RUN pip install --upgrade --no-cache-dir pip
# install packages required for simulation
RUN pip install --no-cache-dir "numpy==1.16.1" "python-dateutil==2.8.0" "scipy==1.2.1" "matplotlib==3.0.2" "networkx==2.2" "pandas==0.24.1" "seaborn==0.9.0"
# packages for web
RUN pip install --no-cache-dir "psycopg2-binary==2.7.7" "sqlalchemy==1.2.18" "Flask==1.0.2" "Flask-WTF==0.14.2" "uuid==1.30" "namesgenerator==0.3" "pika==0.13.0" "Flask-SocketIO==3.3.1" "eventlet==0.24.1" "Flask-RESTful==0.3.7" "schema==0.6.8"

# wo es losgehen soll
ENTRYPOINT ["python"]

# image config
# ist nicht mein Computer, sondern wo es im Container spaeter sein wird
WORKDIR /ProjektQ/

