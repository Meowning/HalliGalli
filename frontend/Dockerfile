FROM node:18 AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . /app

RUN npm run build

FROM nginx:1.21.4-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf.template

ENV BACKEND_HOST=backend
ENV BACKEND_PORT=5000

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
