FROM node:20-alpine AS build

WORKDIR /app

COPY SmartGuard-Vision-Fron/package*.json ./
RUN npm ci

COPY SmartGuard-Vision-Fron/ ./
RUN npm run build

FROM nginx:1.27-alpine

COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
