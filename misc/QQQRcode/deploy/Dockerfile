FROM python:3.12.10-slim-bookworm

RUN echo "deb https://mirrors.ustc.edu.cn/debian bookworm main contrib non-free" > /etc/apt/sources.list && \
    echo "deb https://mirrors.ustc.edu.cn/debian bookworm-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.ustc.edu.cn/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list
RUN apt-get update 

RUN apt-get install -y socat \
    libzbar-dev

RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
    pyzbar Pillow

COPY ./src/ /app
COPY ./flag /flag
COPY ./docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

RUN useradd -m ctf
RUN chown ctf:ctf /app
USER ctf

ENTRYPOINT ["/bin/bash","/app/docker-entrypoint.sh"]