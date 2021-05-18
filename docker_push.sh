#!/bin/bash

sudo docker login --username "mojtabanafez96@gmail.com" --password "c72cc697-deaf-4e4a-9212-582913749385" registry.heroku.com
heroku container:push web -a consultant-iust && heroku container:release web -a consultant-iust