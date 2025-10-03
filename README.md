# Overview

This application is an excercise of how to apply Domain Driven Design, hexagonal architecture and Solid principes with Python, by developing a backend application.

As my background comes from PHP and Symfony, I've developed using the same methodology, and the result is an application with:

- API: I've selected Flask as API library.
- Database management: using Flask migrations, the database is built from the entities. The system creates migrations for build and manage the database.
- Events: the communication between the different services of the application is done by events, so the services are decoupled from the flow.
- Logs: write logs for debug and performing pourposes.
- Exceptions: all exceptions are managed and controled. The are registered in the log and also in the API responses.
- The system reads from external APIs and authenticate by API Key.
- With DDD concepts: Aggregates, Entities, Models, Repository, DTOs, Value Objects.
- Use abstract clases to create interfaces, so I can invert dependencies.

There are several services that perform operations like:

- Read external API
- Save to database, and manage relationships between entites.
- Read from database

# Install

## Requirements

The application requires Docker Desktop to run. In the folder ./docker you can find the Docker configuration.

## Clone the repository

## Start the application

Create network

```bash
docker network create common_network
```



# Development

Basic flow

![image-20250702104815934](.\README.assets\image-20250702104815934.png)

