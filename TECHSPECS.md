# Tech Specs

<img src="./doc/meteo-french-api-logo.png" alt="meteo-french-api-logo" width="200"/>

## Background

We build an API, called _Meteo French API_ that will serve weather information to worldwide connected watches.

The API will be integrated in an already existing backend environment hosted in the cloud and deployed with kubernetes.
The backend environment already has a authentication API OpenID Connect standard, a SQL database, a noSQL database and other APIs. Every watches has the ability to authenticate itself through the OpenID API and access APIs.

We have a `X` active watches that will be clients of the _Meteo French API_ and we estimate `XX` calls per day to our new API. Watches are used all over the world and we have `2` (1 in Europe/Paris, 1 in West USA California) backend environments deployed to support worldwide requests (asumption).

We also have 2 other environments for testing purpose :
* `test`:
To run automatic tests.
* `staging`:
To run manual and performance tests.

Our APIs are developped in Python with Flask framework and we follow a set of development rules, among them :
* document APIs with OpenAPI 3.0 standard
* python lint (TBD)
* unittests
* security mitigation

To develop _Meteo French API_ we will use a third party API dedicated to weather information : [AccuWeather](https://developer.accuweather.com/apis).


## Goals

Develop, document, test and deploy the _Meteo French API_ a micro-service to expose a weather service.
Using this API : https://developer.accuweather.com/apis

In *Python*, using *Flask* with *2 endpoints*:
* `/precipitation?lat={latitude}&long={longitude}`:
Returns a json containing the visibility and Amount of precipitation in the last hour
* `/uv?lat={latitude}&long={longitude}`:
Return current UV index

It must be dockerized and deployed on kubernetes using: `kubectl apply -f my_api.yaml`.

The API will be stateless, so we will use functions rather than classes.

This API must be presented on the Jan 4th 2022, and therefore be ready some days before (Dec 30th 2021 deadline).


## Non-goals

* We suppose we have a authentication micro-service with OpenID Connect standard and won't develop a authentication system. Our API will consume a JWT that will be generated by the authentication service beforehand.
* Due to planning restrictions, the work will focus on the code more than testing, security, deployment and monitoring process and performance optimization. But this document purpose is also to highlight weaknesses of the current implementation and propose improvements.

## Plan / Milestones

- [X] Register for https://developer.accuweather.com/apis and get to know the app with documentation
- [X] Write a AccuWeather API client with the core logics of the _Meteo French API_ in a [Jupyter notebook](./quick_tests/accuweather-client.ipynb)
- [ ] Create the structure of the API with APIFlask
- [ ] Fill the structure with core logics from notebook
- [ ] Generate the OpenAPI spec
- [ ] Write unit tests for core logics functions
- [ ] Write unit tests for API
- [ ] Write `meteo-french-api.yaml` k8s spec to deploy and test to deploy locally with `minikube`.

- [ ] JWT Authentication implemetation and unit tests
- [ ] Deployment in AKS in 1 `test` environment
- [ ] Static code analysis for security
- [ ] Integrate monitoring features (Sentry, ELK, Prometheus)

- [ ] Deployment in `staging`
- [ ] End-to-end validation in `staging` with connected watches *(need the API client development to be ready)*
- [ ] Load and performance tests in `staging`
- [ ] Deployment in `prod` worldwide
- [ ] Monitoring during _pilote_ period: The watch software version that include the weather client feature is deployed only on 10% of all the units
- [ ] Scale pilote: 10% (2 weeks) => 50% (2 weeks) => 100%

## KPI / Monitoring

* Sentry for logs

Grafana board (To be defined, we'll do the same as the other APIs) :
* Status codes (no-go if `2XX < 80%` ?)
* Time response per endpoint (objective: `200ms` ?)
* Requests history (per hour)
* Requests geography

Kibana board
* Requests per user id (info from JWT) => for security purpose to check they are known authenticated users.
* Lat/Lng (in request params) vizualisation ? => it might drive possible optimizations


## Improvement ideas

* Asynchronous calls to AccuWeather API
* Approximate latitude and longitude that will have the same weather information, and cache locationKey and weather info to respond faster. For example all `(lat, long)` in the bounding box `[((48.87, 2.30)), ((48.88, 2.31))]` will be approximate to `(48.875, 2.305)` and will be considering having the same location key. This will help a lot because in a city there is a concentration of API clients (watches) which will get the same weather results.
* Approximation with a boundary box size in meters (because the conversion between latitude or longitude distance and meters distance is not constant, it depends on where you are on earth).
* parameter in the endpoint get request to choose the unit system (metric or imperial) to let the end user the possibility to set its 


## Open Questions

- [ ] How to store our AccuWeather Token securely ? `.env` files ? [git-secret](https://git-secret.io/)
