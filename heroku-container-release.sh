#!/bin/bash
imageId=$(docker inspect registry.heroku.com/consultant-se-iust/consultant --format={{.Id}})
payload='{"updates":[{"type":"web","docker_image":"'"$imageId"'"}]}'
curl -n -X PATCH https://api.heroku.com/apps/consultant-se-iust/formation \
-d "$payload" \
-H "Content-Type: application/json" \
-H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
-H "Authorization: Bearer b7a69d7c-73a7-4edd-bb12-2c0b52a2094f"