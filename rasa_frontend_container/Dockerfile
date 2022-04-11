FROM node:16.14.2 as build-stage
WORKDIR /app/UI
COPY UI/package*.json ./
RUN npm install
COPY UI/ .
RUN npm run build
RUN rm -f /app/static/src/vue/dist/index.html
ADD replacement_index/index.html /app/static/src/vue/dist/index.html

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/static/src/vue/dist /usr/share/nginx/html

