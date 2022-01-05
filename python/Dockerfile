FROM python:3.8.6

USER root

RUN apt-get update && \
    apt-get -y install locales && \
    apt-get -y install default-mysql-client && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8 && \
    mkdir py-work

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

# python package
RUN pip install --upgrade pip && \
    pip install sqlalchemy && \
    pip install mysqlclient && \
    pip install twisted && \
    pip install scrapy==2.3.0 && \
    pip install scrapy_splash && \
    pip install japanera && \
    pip install mojimoji 

CMD [ "/bin/bash" ]
