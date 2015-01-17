FROM ubuntu
MAINTAINER Eslam El Husseiny <eslam.husseiny@gmail.com>

RUN apt-get update 
RUN apt-get install -y git python-pip
RUN pip install boto

RUN echo "#!/bin/bash" > /root/run.sh
RUN echo "git clone https://github.com/EslamElHusseiny/test.git /root/test" >> /root/run.sh
RUN echo "python /root/test/engine.py" >> /root/run.sh

ENV AWS_ACCESS_KEY_ID none
ENV AWS_SECRET_ACCESS_KEY none

CMD ['/root/run.sh']