# Flask Api Boilerplate

Boilerplate code for flask powered backend applications
Includes a postgres for a database, celery for bacgkround tasks, and redis as a message broker.
See `.env.example` for the env set up. You may need to add a setting in `config.settings` if its an app related
env variable

## Getting set up

### Build and run the app

1. Change .env.example to .env
2. Add/change the necessary env variables needed for the app
3. Open a terminal configured to run Docker and run:
   - docker-compose down -v
   - docker-compose up --build
   - docker-compose exec web app db reset --with-testdb
   - docker-compose exec web app flake8
   - docker-compose exec web app test

## Database Migrations

While the web container is running, execute the following alembic commands

1. Create a migration file:
   - docker-compose exec web alembic revision -m "your message here"
   - See the newly created migration file inside `/app/migrations/versions/`. you will need to write the code for the `upgrade` and `downgrade` functions yourself

2) Run the migration:

   - docker-compose exec web alembic upgrade head
     - "head" will use the latest revision
       **this will only update the database schema, you will ofcourse need to update the source code to use this new table**

3) Downgrade migration:

   - docker-compose exec web alembic downgrade -1
     - the "-1" means we're rolling back 1 revision
       **you can also downgrade to a specific revison ID**

4) View migration history:

   - docker-compose exec web alembic current

     - this command will return the revision ID in use based on the current state of the database

   - docker-compose exec web alembic history --verbose
     - will return revision ID's and their related files

5) Auto generate migrations from existing models:
   alembic will determine the difference between the sqlalchemy models in the flask app and attempt to generate migrations based on the difference. lets say you added a "foo" column users model in the source code
   - docker-compose exec web alembic revision --autogenerate -m "add foo cloumn to users"
     - this will create a migration file that will include the new sqlalchemy model field in our database schema
   - docker-compose exec web alembic upgrade head
     - run the new migration
