FROM node:16.14.2 as build-stage
RUN npm install -g http-server
WORKDIR /app/UI
COPY UI/package*.json ./
RUN npm install
COPY UI/ .
RUN npm run build

# production stage
FROM nginx as production-stage
RUN mkdir /app
COPY --from=build-stage /app/static/src/vue/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
