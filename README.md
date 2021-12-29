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

The result is found at [meteofrenchapi/openapi.yaml](./meteofrenchapi/openapi.yaml)

## Run unit tests

```
./run_docker_local.sh python -m unittest discover meteofrenchapi
```

## Push docker image to registry

```
./push_docker.sh <registry/image_name>
```

## Deploy in minikube

Test `minikube` and `kubectl` are installed
```
minikube version
kubectl version
```

Create a `mfapi-secret.yaml` file with required secrets with the following template
```
apiVersion: v1
kind: Secret
metadata:
  name: mfapi-secret
type: Opaque
data:
  SECRET_KEY: <pass_base64>
  ACCUWEATHER_TOKEN: <pass_base64>
```

Note: The base64 encoding password can be generated with the following command : `echo -n "password" | base64`

Apply secret file:
```
kubectl apply -f mfapi-secret.yaml
```

Deploy application:
```
kubectl apply -f mfapi.yaml
```

View the API with the command `minikube service mfapi-service`
