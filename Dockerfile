FROM node:16.14.2 as build-stage
RUN npm install -g http-server
WORKDIR /app
COPY UI/package*.json ./
RUN npm install
COPY UI/ .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /static/src/vue/dist/ /usr/share/nginx/html/
EXPOSE 80
