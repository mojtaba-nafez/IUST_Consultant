#!/bin/bash

sudo docker login --username "mojtabanafez96@gmail.com" --password "b7a69d7c-73a7-4edd-bb12-2c0b52a2094f" registry.heroku.com
sudo docker tag consultant-iust:latest registry.heroku.com/consultant-iust/web
if [ $TRAVIS_BRANCH == "Dockerization" ] && [ $TRAVIS_PULL_REQUEST == "false" ]; then sudo docker push registry.heroku.com/consultant-se-iust/consultant; fi

chmod +x heroku-container-release.sh
sudo chown $USER:docker ~/.docker
sudo chown $USER:docker ~/.docker/config.json
sudo chmod g+rw ~/.docker/config.json

./heroku-container-release.sh
