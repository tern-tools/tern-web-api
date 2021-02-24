# Tern API

Tern api is Web API for [Tern](https://github.com/tern-tools/tern). 
This project is still a PoC phase, so it may have bugs and apis are subject to change.

# Getting Started

## Getting Started with Docker
If you already have Docker installed, you can run Tern API by building a container with the Dockerfile provided and the `docker_run.sh` script:

Clone this repository:
```
$ git clone https://github.com/tern-tools/tern-api.git
```

Build the Docker image (called `tern-api` here). You may need to use sudo:
```
$ docker build -f docker/Dockerfile -t tern-api .
```

Run the script `docker_run.sh`. You may need to use sudo.

```
$ ./docker_run.sh tern-api
```

To try producing a report via a sample Web UI, access to 127.0.0.1:5000/webui from browser.
Swagger UI is also available on 127.0.0.1:5000/.

What the `docker_run.sh` script does is run the built container as privileged.

*WARNING:* privileged Docker containers are not secure. DO NOT run this container in production unless you have secured the node (VM or bare metal machine) that the docker daemon is running on.
