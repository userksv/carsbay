
# gunicorn_config.py

bind = "0.0.0.0:8000"
module = "carsbay_project.wsgi:application"

workers = 4  # Adjust based on your server's resources
worker_connections = 1000
threads = 4

certfile = "/etc/letsencrypt/live/www.carsbay.com/fullchain.pem"
keyfile = "/etc/letsencrypt/live/www.carsbay.com/privkey.pem"