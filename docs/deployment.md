## Deployment to Heroku

1. Install the heroku CLI

    ```bash
    brew tap heroku/brew && brew install heroku
    ```

2. Login with your heroku credentials

    ```bash
    heroku login
    ```

3. Create your application

    ```bash
    heroku apps:create --buildpack heroku/python
    ```

4. Add redis add-on for celery worker

    ```bash
    heroku addons:create heroku-redis -a your_app_name
    ```

5. Add PostgreSQL add-on for database

    ```bash
    heroku addons:create heroku-postgresql
    ```

6. Verify `REDIS` and `DATABASE` exist

    ```bash
    heroku addons
    ```

    ![Addons](../images/heroku_addons.png)

7. Run the line below for each variable (except `DATABASE_URL` and `REDIS_URL`) in [configuration guide](configuration.md)
    
    ```bash
    heroku config:set VARIABLE_NAME=variable_value
    ```

8. Push the code to heroku
    
    ```bash
    git push heroku master
    ```

9. Start the celery worker on a dyno

    ```bash
    heroku ps:scale worker=1
    ```

10. Open the application

    ```bash
    heroku open
    ```
