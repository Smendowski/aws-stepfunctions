docker build -t fetch-data-lambda -f fetch-data/Dockerfile fetch-data
docker run -p 9000:8080 fetch-data-lambda
