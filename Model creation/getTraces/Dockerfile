FROM ubuntu:latest

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update
RUN echo "wireshark-common wireshark-common/install-setuid boolean false" | debconf-set-selections
RUN apt install -y python3 python3-pip tshark xvfb tcpdump

RUN pip3 install pyshark pandas selenium netifaces

COPY imageGeneration/google-chrome-stable_current_amd64.deb /root/google-chrome-stable_current_amd64.deb
RUN apt install -y /root/google-chrome-stable_current_amd64.deb
RUN rm /root/google-chrome-stable_current_amd64.deb

COPY imageGeneration/chromedriver /bin/chromedriver
COPY imageGeneration/startingScript.sh /root/startingScript.sh
COPY imageGeneration/getTraces.py /root/getTraces.py

RUN chmod +x /root/startingScript.sh
RUN chmod +x /root/getTraces.py
RUN chmod +x /bin/chromedriver

ENTRYPOINT [ "/root/startingScript.sh" ]