FROM hepsw/cvmfs-cms

MAINTAINER lkreczko@gmail.com

RUN yum install -y wget glibc gcc
RUN useradd tquark
RUN mkdir /software && chown -R tquark /software
RUN mkdir /project && chown -R tquark /project
WORKDIR /project

COPY ./bin /project/bin
COPY ./data /project/data
COPY ./interface /project/interface
COPY ./plugins /project/plugins
COPY ./python /project/python
COPY ./src /project/src
COPY ./test /project/test
COPY ./requirements.txt /project/.
COPY ./setup.json /project/.
COPY ./BuildFile.xml /project/BuildFile.xml

ENV DEBUG 1
RUN source bin/env.sh

# need to execute env.sh and ntp setup in CMD
# as CVMFS needs 'privileged' rights,
# but cannot do that when building the container
CMD ["/bin/bash", "-c", "source bin/env.sh; ntp setup"]
