FROM python:3.12 as base-img
COPY ./requirements.txt /code/requirements.txt
COPY ./supervisor.conf  /etc/supervisor/conf.d/supervisor.conf
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN apt update && apt install -y supervisor socat

FROM base-img
COPY . /code
CMD ["/usr/bin/supervisord"]
