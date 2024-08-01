FROM nginx:latest

COPY static/ /usr/share/nginx/html/

# copy the custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf


EXPOSE 80