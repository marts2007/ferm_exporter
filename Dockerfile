FROM ubuntu:18.04
RUN apt-get update -y && \
    apt-get install -y python3.7 python3-pip
RUN python3.7 -m pip install pip

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
