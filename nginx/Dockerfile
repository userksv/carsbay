FROM nginxproxy/nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY vhost.d/default /etc/nginx/vhost.d/default
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]