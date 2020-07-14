# Ops Status

This is the django project for Ops Status to check your favorite tools for their status and output failures directly in Slack.

## Getting Started

Use docker for local development environment setup:

```
    docker-compose up -d
```

Use cli to interact with the container:

```
    docker-compose exec web bash
```

Then you can create a superuser account:

```
    python manage.py createsuperuser
```
