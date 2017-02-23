# webapp
Web app for amazon recommender system

## Architecture

web -> nginx reverse proxy -> flask app server <-> postgres/redis DB

## Setup

```
docker-compose build
docker-compose up
```

Then it should be running on port 3000

## Misc

Shell:

```
docker-compose run web /bin/ash
```