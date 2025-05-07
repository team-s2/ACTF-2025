FROM node:23

WORKDIR /app
COPY src .

COPY ./debian.sources /etc/apt/sources.list.d/debian.sources

RUN apt-get update && apt-get install -y pandoc chromium
RUN npm install

ENV PROD=1

CMD ["node", "app.js"]