aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 730335229700.dkr.ecr.ap-northeast-2.amazonaws.com

docker pull 730335229700.dkr.ecr.ap-northeast-2.amazonaws.com/carsbay:nginx-proxy
docker pull 730335229700.dkr.ecr.ap-northeast-2.amazonaws.com/carsbay:web
docker pull 730335229700.dkr.ecr.ap-northeast-2.amazonaws.com/carsbay:websocket