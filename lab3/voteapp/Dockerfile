## Base Image with Python3.6 and Flask 
FROM tiangolo/uwsgi-nginx-flask:python3.6

## Install redis python lib
RUN pip install redis

## Copy entire app into /app
ADD /votecode /app

## expose port 80 
EXPOSE 80