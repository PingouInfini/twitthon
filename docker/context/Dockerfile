FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y openssh-server  && \
    mkdir /var/run/sshd  && \
    echo 'root:root' |chpasswd && \
    apt-get update && \
    apt-get install -y python3-pip && \
    apt-get install -y curl && \
    apt-get install -y unzip && \
    apt-get install -y vim
    #sed -ri 's/^PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
    #sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config && \

COPY sshd_config /etc/ssh/sshd_config
RUN mkdir /app
COPY dockerdist/*.* /app/
RUN mkdir /app/src
COPY dockerdist/src /app/src

RUN pip3 install --no-cache-dir -r /app/requirements.txt

RUN  apt-get -y autoclean && apt-get -y autoremove && \
     apt-get -y purge $(dpkg --get-selections | grep deinstall | sed s/deinstall//g) && \
     rm -rf /var/lib/apt/lists/*

RUN chmod 755 ./app/entrypoint.sh

ENTRYPOINT ["./app/entrypoint.sh"]