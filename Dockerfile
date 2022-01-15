FROM ubuntu:latest
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt install -y curl wget unzip qbittorrent-nox megatools
RUN apt install net-tools
RUN apt-get install iptables-persistent -y
RUN wget https://github.com/fedarovich/qbittorrent-cli/releases/download/v1.7.21116.1/qbt-linux-x64-1.7.21116.1.tar.gz
RUN tar xf qbt-linux-x64-1.7.21116.1.tar.gz
RUN apt-get install -y aria2 git python3 python3-pip unzip 
RUN apt install -y make python build-essential
RUN apt-get install unrar
RUN curl https://rclone.org/install.sh | bash
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash
RUN wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip && unzip ngrok-stable-linux-amd64.zip && mv ngrok /usr/local/bin/ngrok
RUN wget https://github.com/nzbget/nzbget/releases/download/v21.0/nzbget-21.0-src.tar.gz
RUN tar -zxvf nzbget-21.0-src.tar.gz
RUN apt-get update && apt install nodejs -y
RUN npm config set unsafe-perm true
RUN apt install rtorrent screen -qq -y
RUN mkdir -p -m 666 /{content/rTorrent/,root/.rTorrent_session}
RUN mkdir -p -m 777 /root/.Flood/
RUN curl -s https://raw.githubusercontent.com/SameerkumarP/Rc-v-2.0/master/res/rtorrent/rtorrent.rc -o /root/.rtorrent.rc
RUN chmod 666 /root/.rtorrent.rc
RUN git clone https://github.com/MinorMole/FloodLab.git /root/.Flood/
RUN npm install --prefix /root/.Flood
RUN npm update 
RUN npm rebuild --prefix /root/.Flood
RUN mkdir /bot
RUN chmod 777 /bot
COPY . /bot
WORKDIR /bot
RUN chmod -R 777 /bot
RUN npm install
CMD node server
