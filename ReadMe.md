# How to try out your project

To run the project, open a `terminal` in your projects root-folder, then run the following command:
```bash
docker compose up --force-recreate
```

You will see console output notifying you that your API, Backend, and Frontend are running.

You can now navigate to your `frontend` in your browser at `http://localhost`, reach your `backend` at `localhost:5000`, and find a `postgresql` database at `localhost:5432`.

In case one of the dependencies was not started, you will find Error messages in the same `terminal` that was used to issue `docker compose up --force-recreate`

To shut down the project, open a `terminal` in your projects root-folder, then run the following command:
```bash
docker compose stop
```
