FROM python:3.7

MAINTAINER "Alexey Lukyanov"

WORKDIR /opt

# /opt/setup.py
# /opt/PACKAGE
COPY setup.py /opt/
COPY tw_streamer /opt/tw_streamer

RUN pip --no-cache-dir install redis \
 && pip --no-cache-dir install tweepy \
 && python setup.py sdist \
 && pip --no-cache-dir install dist/tw_streamer* \
 && rm -r dist setup.py tw_streamer

CMD "python -m tw_streamer.launcher"
