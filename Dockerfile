FROM node:16.14.2 as build-stage
WORKDIR /app
COPY UI/ /app
RUN npm install
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
