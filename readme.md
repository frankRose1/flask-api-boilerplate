# Flask Api Boilerplate
Boilerplate code for flask powered backend applications
Includes a postgres for a database, celery for bacgkround tasks, and redis as a message broker.
See ```.env.example``` for the env set up. You may need to add a setting in ```config.settings``` if its an app related
env variable

## Getting set up
### Build and run the app
1) Change .env.example to .env
2) Add/change the necessary env variables needed for the app
3) Open a terminal configured to run Docker and run:
    - docker-compose down -v
    - docker-compose up --build
    - docker-compose exec web app db reset --with-testdb
    - docker-compose exec web app flake8
    - docker-compose exec web app test