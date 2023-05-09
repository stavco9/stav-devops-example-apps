REPO_NAME='stav-poc'
REGION='us-east-1'
REGISTRY="882709358319.dkr.ecr.${REGION}.amazonaws.com"
VERSION='1.0'

docker build -t ${REPO_NAME} .

aws ecr describe-repositories --repository-names ${REPO_NAME} || \
 aws ecr create-repository --repository-name ${REPO_NAME}

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin  ${REGISTRY}

docker tag ${REPO_NAME} ${REGISTRY}/${REPO_NAME}:${VERSION}
docker push ${REGISTRY}/${REPO_NAME}:${VERSION}
