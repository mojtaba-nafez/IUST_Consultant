# IUST_Consultant# Consultant

# important point:
if update user types => you must update 3 file => app User(model.py, serializer.py)  app channel(view.py: class SuggestionChannel) 



Heroku admin page:
admin
admin.iust.ac.ir
admin12345

heroku container:push web  --app consultant-iust

python manage.py makemigrations User calendar_ channel chat_room message request


docker-compose run --rm consultant sh -c "python manage.py createsuperuser"

docker-compose run --rm consultant sh -c "python manage.py test"
docker-compose run --rm consultant sh -c "python manage.py makemigrations User calendar_ channel chat_room message request"
  docker-compose run --rm consultant sh -c "python manage.py migrate"




docker stop consultant_postgresql && docker rm consultant_postgresql && docker stop consultant && docker rm consultant

add ('auth', '__latest__') to dependency of migrations 



see django sqlite db:
sqlite3 db.sqlite3
.tables

SELECT sql FROM sqlite_master WHERE tbl_name = 'channel_channel' AND type = 'table'



# search-for-channel : 
http://localhost:8000/channel/search-for-channel/?query=&search_category=Lawyer    : return all channel in Lawyer category

http://localhost:8000/channel/search-for-channel/?query=         : return all channel



# problem :
1- In get channel subscribers:  API is just for channel owner and admin   
2- channel has not avatar 
3- searchs API han not return avatar of channels
4- channels has not image fields
5- user have avatoar field but it's not force to get image from user(normal user or consultant)  # Consultant

# important point:
if update user types => you must update 3 file => app User(model.py, serializer.py)  app channel(view.py: class SuggestionChannel) 


Heroku admin page:
admin
admin.iust.ac.ir
admin12345


python manage.py makemigrations User calendar_ channel chat_room message 


add ('auth', '__latest__') to dependency of migrations 



see django sqlite db:
sqlite3 db.sqlite3
.tables

SELECT sql FROM sqlite_master WHERE tbl_name = 'channel_channel' AND type = 'table'



# search-for-channel : 
http://localhost:8000/channel/search-for-channel/?query=&search_category=Lawyer    : return all channel in Lawyer category

http://localhost:8000/channel/search-for-channel/?query=         : return all channel



# problem :
1- In get channel subscribers:  API is just for channel owner and admin   
2- channel has not avatar 
3- searchs API han not return avatar of channels
4- channels has not image fields
5- user have avatoar field but it's not force to get image from user(normal user or consultant)  














version: '3'

services:
  consultant:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: consultant
    volumes:
      - .:/consultant
      - consultant_static_volume:/consultant/static
      - consultant_files_volume:/consultant/files
    restart: always
    ports:
      - "8000:8000"
    networks:
      - consultant_network
      - nginx_network
    depends_on:
      - consultant_postgresql
  consultant_postgresql:
    image: postgres:12
    container_name: consultant_postgresql
    volumes:
      - consultant_postgresql:/var/lib/postgresql/data
    restart: always
    env_file: .env
    ports:
      - "5432:5432"
    networks:
      - consultant_network

volumes:
  consultant_postgresql:
    external: true
  consultant_static_volume:
    external: true
    consultant_files_volume:
    external: true
networks:
  consultant_network:
    external: true
  nginx_network:
    external: true












docker-compose up -d
docker-compose up
docker volume create consultant_files_volume
docker network create nginx_network
docker ps -a
docker logs consultant_postgresql


Remove DB:
docker stop consultant_postgresql
docker rm consultant_postgresql
docker-compose up


docker exec -it consultant_postgresql psql -U postgres -W postgres
docker stop consultant_postgresql && docker rm consultant_postgresql && docker stop iust_consultant_consultant_1 && docker rm iust_consultant_consultant_1

docker stop consultant_postgresql && docker rm consultant_postgresql && docker stop consultant && docker rm consultant
  