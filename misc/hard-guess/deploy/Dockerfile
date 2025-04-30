FROM --platform=linux/amd64 python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y openssh-server sudo gcc && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m KatoMegumi && \
    echo 'KatoMegumi:Megumi960923' | chpasswd && \
    echo 'root:A7EEE9C3-E50B-424A-A84A-6060E48AC70F' | chpasswd

RUN mkdir /var/run/sshd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

COPY hello.c /tmp/hello.c
COPY flag /root/flag

RUN gcc /tmp/hello.c -o /opt/hello && \
    rm /tmp/hello.c

RUN chown root:root /opt/hello && \
    chmod 4755 /opt/hello

RUN chown root:root /root/flag && \
    chmod 4700 /root/flag

EXPOSE 22

CMD ["sh", "-c", "/usr/sbin/sshd -D"]