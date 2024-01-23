FROM  --platform="linux/amd64" nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY /etc/letsencrypt/live /etc/letsencrypt/live

# RUN chmod 644 /etc/letsencrypt/live/carsbay.one/fullchain.pem
# RUN chmod 600 /etc/letsencrypt/live/carsbay.one/privkey.pem


EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]