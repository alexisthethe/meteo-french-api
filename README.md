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
