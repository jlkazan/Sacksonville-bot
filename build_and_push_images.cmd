docker-compose build bot-lambda

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 117519952951.dkr.ecr.us-east-1.amazonaws.com

docker tag  sacksonville_bot_lambda:latest 117519952951.dkr.ecr.us-east-1.amazonaws.com/sacksonville-bot-lambda:latest
docker push 117519952951.dkr.ecr.us-east-1.amazonaws.com/sacksonville-bot-lambda:latest