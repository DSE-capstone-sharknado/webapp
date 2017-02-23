# webapp
Web app for amazon recommender system

## Architecture

web -> nginx reverse proxy -> flask app server <-> postgres/redis DB

I image this acting like an REST API where you can get rankings like:

```
GET /users/[userid]/rankings?limit=10
``

which would return the top ten items in json:

```
{
  [
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r},
    {asin: "xxxxxx", image_url:"http://...jpg", rank: r.r}
  ]
}
```

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