# IMDb Analyzer

A work in progress. More documentation on the way!

## Learning goals

Originally intended to be a lightweight IMDb scraper, this project has evolved into a microservices learning experience. In this project, I hope to learn more about: 

- Microservices architectural design
    - Designation of responsibilities
    - Well-defined data flows (Istios)
    - Abstraction of common infrastructure
    - etc.
- Docker containerization
- Inter-container communication (RESTful vs. RPC)
- Container orchestration (Kubernetes)
- Golang and its advantages in concurrency
- CI / CD

## Getting started

Please follow the following commands to test the application. Some of the following instructions are mac/linux specific.

Before tesing, please ensure the following dependencies are installed:
- [docker](https://docs.docker.com/v17.12/docker-for-mac/install/#download-docker-for-mac)
- [brew](https://brew.sh)
- [node](https://treehouse.github.io/installation-guides/mac/node-mac.html)

To start up the environment, go to the root directory and run

```bash
make run-demo   # that starts up the environment and loads sample data
# or
make run        # that only starts up the environment

# workaround: start webapp locally
# we discard this step when we solve inter-container communication 
cd src/app
make init
make run
```

## Visuals

**UI**
![stdui](docs/static/sample_ui.png)

**CLI**
![stdout](docs/static/sample_stdout.png)
