FROM  --platform="linux/amd64" nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY /etc/letsencrypt /etc/letsencrypt
COPY /var/lib/letsencrypt /var/lib/letsencrypt

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]