# studying-flask
Flask RESTful API with JWT Authentication 

### API Documentation
You need to know how to test this API? Access the API Documentation, with examples and importants informations [here](https://documenter.getpostman.com/view/12464969/T1LVA4k8?version=latest)

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/d97f2b3738ec597d9c54)

#

### Run this project
*This project was developed in an environment with Ubuntu 18.04, Docker 19.03.12 and docker-compose 1.26.2. But, you can run in any environment with Docker 19+ and docker-compose 1.25+.*

Inside the project's root folder, run:
```
docker-compose up
```

### Running dockerized tests
Outside the container, you can run the following commands to test the code inside the docker

If you want just to execute the tests, run:
```commandline
docker container exec flask-api python -m unittest -v
```

If you want to see the test coverage level, run:
```commandline
docker container exec flask-api coverage run --source=app -m unittest discover -s tests/ -v

docker container exec flask-api coverage report
```