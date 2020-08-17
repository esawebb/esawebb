# ESA Hubble

Djangoplicity CMS for the ESA Hubble Project (https://www.spacetelescope.org/)

## Requirements

- Docker
- Docker Compose

## Development

### Cloning the repository

In your terminal run the command:

```` 
git clone https://gitlab.com/esahubble/esahubble.git
````

### Running the project

All the configuration to start the project is present in the docker-compose files and Dockerfile,
then at this point a single command is required to download all the dependencies and run the project:

```` 
docker-compose up
````

> The previous command reads the config from docker-compose.yml and docker-compose.override.yml, because of the naming convention of docker-compose

When the process finishes, the CMS will be available at *`localhost:8000`*

To stop containers press:

```
CTRL + C
```

If the dependencies change, you should recreate the docker images and start the containers again with this command:

```` 
docker-compose up --build
````

### Additional commands

Inside the `Makefile` there are multiple command shortcuts, they can be run in UNIX systems like this:

```
make <command-name>
```

E.g.

```
make migrate
```

> In windows you can just copy and paste the related command

### The demo seed

The project contains a _demo seed_ that can be loaded in order to populate example data to the database, to load the demo data run the following command while the containers are running:

```
docker exec -it hubble ./manage.py loaddata demo
```

or

```
make demofixture
```
