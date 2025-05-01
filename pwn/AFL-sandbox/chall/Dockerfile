FROM ubuntu:22.04

# to tsinghua apt sources
RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list

RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd
RUN apt-get install -y python3 libseccomp-dev

RUN useradd -m ctf

WORKDIR /home/ctf

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./wrapper.py /home/ctf/wrapper.py
COPY ./start.sh /start.sh
COPY ./flag /home/ctf/flag
COPY ./afl-fuzz /home/ctf/afl-fuzz
COPY ./harness /home/ctf/harness

RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail
RUN chmod +x /start.sh /home/ctf/afl-fuzz /home/ctf/harness
RUn mkdir -p /home/ctf/input /home/ctf/output
RUN echo -n b"\x00\x00\x00\x00" > /home/ctf/input/0

RUN chown -R root:ctf /home/ctf && chmod -R 750 /home/ctf && chmod 740 /home/ctf/flag
RUN chown -R root:ctf /home/ctf/input && chmod -R 750 /home/ctf/output
RUN chown -R ctf:ctf /home/ctf/wrapper.py
RUN chmod u+s /home/ctf/wrapper.py

EXPOSE 9999

CMD ["/start.sh"]
