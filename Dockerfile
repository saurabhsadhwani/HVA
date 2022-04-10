FROM node:16.14.2 AS BASE

WORKDIR /app

COPY UI/ /app

RUN npm install
