# meteo-french-api
Meteo French API

## Mission

Develop a micro-service to expose a weather service.
Using this API : https://developer.accuweather.com/apis

In python, using Flask. 
Implement a python service with two endpoints:
* `/precipitation?lat={latitude}&long={longitude}`:
Returns a json containing the visibility and Amount of precipitation in the last hour
* `/uv?lat={latitude}&long={longitude}`:
Return current UV index

It must be dockerized and deployed on kubernetes using: `kubectl apply -f my_api.yaml`

## Tech Specs

Read [Tech Specs](TECHSPECS.md) that document the specification and milestones of the API from development to deployment.

## Run locally

Set environment variables secrets in a `.env.secret` file (check in the [.env.dev](.env.dev) file which ones are to be set)

Build the docker image and run the app locally with
```
./run_docker_local.sh
```

Now you can visit http://localhost:8000/docs to view the Swagger UI of the app (only available in `dev` environment)

## Generate the OpenAPI spec

```
./run_docker_local.sh flask spec
```

The result is found at `meteofrenchapi/openapi.yaml`

