# wazo-router-confd

wazo-router-confd provides REST API for the C4 infrastructure.

## Installing wazo-router-confd

The server is already provided as a part of [Wazo](http://documentation.wazo.community).
Please refer to [the documentation](http://documentation.wazo.community/en/stable/installation/installsystem.html) for
further details on installing one.

## Running with wazo-auth
```
$ make start-auth
```
Will start all the needed components to use confd with portal UI.
```
$ make setup-auth
```
Will insert the needed tenant uuids to use with wazo-auth and portal.

## Tests

### Running unit tests

```
$ tox --recreate -e py37
```

## Docker

The official docker image for this service is `wazo-platform/wazo-router-confd`.


### Getting the image

To download the latest image from the docker hub

```sh
docker pull wazo-platform/wazo-router-confd
```

### Running wazo-router-confd

```sh
docker run wazo-platform/wazo-router-confd
```

### Building the image

Building the docker image:

```sh
docker build -t wazo-platform/wazo-router-confd .
```

