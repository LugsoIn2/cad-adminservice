FROM python:3.9
#Docker doesn't buffer the output and that you can see the output 
#of the app in real-time.
ENV PYTHONUNBUFFERED 1

#setup gunicorn
RUN pip install gunicorn

# setup nginx
RUN apt-get update
RUN apt-get install -y nginx
COPY ./nginx/proxy-adminservice.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/proxy-adminservice.conf \
/etc/nginx/sites-enabled/proxy-adminservice.conf & \
rm /etc/nginx/sites-enabled/default

# copy service source
RUN mkdir /adminservice
WORKDIR /adminservice
COPY ./adminservice .
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# collect all static files
WORKDIR /adminservice/adminservice
RUN python /adminservice/manage.py migrate
RUN python /adminservice/manage.py collectstatic --noinput

WORKDIR /adminservice
EXPOSE 80

# run nginx + gunicorn
CMD (gunicorn --bind 127.0.0.1:8000 --user www-data --workers=2 adminservice.wsgi) & \
nginx -g "daemon off;"