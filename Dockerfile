FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install git -y && \
    apt-get install python -y && \
    apt-get install python3 -y && \
    apt-get install python-pip -y && \
    apt-get install python3-pip -y && \
    apt-get install python-dev -y && \
    apt-get install python3-dev -y && \
    apt-get install build-essential -y && \
    apt-get install libssl-dev -y && \
    apt-get install libffi-dev -y && \
    apt-get install libxml2-dev -y && \ 
    apt-get install libxslt1-dev -y && \
    apt-get install zlib1g-dev -y

RUN git clone https://github.com/mvelazc0/PurpleSpray.git /tmp/purplespray

WORKDIR /tmp/purplespray

RUN pip3 install -r requirements.txt
RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install impacket
RUN rm -r /root/.cache

ENTRYPOINT [ "python", "PurpleSpray.py" ]