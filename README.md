# Math Microservice API

Maxim Dragos, Data Engineer

- A FastAPI microservice for computing mathematical operations, such as: 
power, factorial, N-th Fibonacci number.


- It uses MVCS principles, Pydantic for request/response validation, logs requests to SQLite, caches in memory, and offers Docker containerization, RabbitMQ logging, API-Key authorization and Prometheus monitoring.

## Features perspective

- **Endpoints**:
- POST /api/pow -> compute a^b
- POST /api/factorial -> compute n!
- POST /api/fibonacci -> compute n-th Fibonacci number


- **Database, logging to SQLite**:
- Every API call is logged in requests.db (requests_logs table) with operation, input, result and HTTP status code.


- **Interactive docs**:
- Swagger UI at /docs for live testing.


- **Backend**: 
- FastAPI application(app.py)


- **Containerization**: 
- Dockerfile and .dockerignore for portable builds


- **RabbitMQ logging**:
- Async publish of each log entry to a math_logs fanout


- **API-Key Authorization**
- Header check (X-API-Key) to protect endpoints


- **Prometheus Monitoring**
- Exposes /metrics on port 8001 for requests counts and latency histogram


- **Caching**: 
- In memory cache avoid recomputation for repeated requests


## Architecture breakdown:

- **Models**(math_service/models/)
- requst_log_model.py: initializes SQLite schema and provides log_to_db()


- **Schemas**(math_service/schemas/)
- math_schema.py: Pydantic models for request/response
- log_schema.py: Pydantic omdel for log entry


- **Services**(math_service/services/)
- math_services.py: business logic (power, factorial, Fibonacci) and caching
- messaging_service.py: publishes log entries to RabbitMQ


- **Controllers**(math_service/controllers)
- math_controller.py: defines /api/* endpoints, orchestrates service calls, logging, publishes to RabbitMQ


- **Views & App Entry**
- math_service/app.py: sets up FastAPI, includes router, adds middleware for Prometheus, mounts /metrics, and applies API-Key dependency.


- **Workers**(math_service/workers/)
- rabbit_consumer.py: consumer that reads from math_logs exchange and prints messages


## Working principle
- **Client** sends a request to an endpoint (/api/pow) by Swagger UI, curl, or HTTP client with valid X-API-Key.


- **Middleware** checks API Key, records start time.


- **Controller** (math_controller.py) 
- Receives the request
- Validates the input using Pydantic
- Calls service function in math_services.py
- receives result
- Logs to SQLite(log_to_db())
- Publishes log entry to RabbitMQ(publish_log())


- **Middleware** measures latency and increments Prometheus counters.


- **App** returns JSON response { "result": <value> }


- **Consumer** used by RabbitMQ and process logs asynchronously


## Content
**Code**
- math_service/app.py -> FastAPI app entrypoint(view), metrics, auth


- math_service/models/request_log_model.py -> SQLite logging


- math_service/schemas/math_schema.py & log_schema.py -> Pydantic models


- math_service/services/math_services.py & messaging_service.py -> logic and RabbitMQ


- math_service/controllers/math_controller.py -> endpoints


- math_service/workers/rabbit_consumer.py -> RabbitMQ consumer


**Config & Docs**
- requirements.txt -> Python dependencies
- Dockerfile & .dockerignore -> container build
- docker-compose.yml -> orchestrate FastAPI + RabbitMQ


**Data**
- requests.db -> SQLite database file


**Tests**
- test_math_service.py -> unit test for service layer



## How to run the server:
**Locally**
- 1.Activate and install
- .venv\Scripts\Activate
- pip install -r requirements.txt


- 2.Start FastAPI
- uvicorn math_service.app:app --reload


- 3.Browse docs
- enter on http://127.0.0.1:8000/docs


- 4.Try
- curl -X POST http://127.0.0.1:8000/api/pow \ -H "Content-Type: application/json" \ -d '{"a":2, "b":8}'


- 5.Logs inspection
- After server has stopped, open requests.db with any SQLite GUI to see requests_logs entries.




## Build and run the Docker container
- Command that tell Docker to build an image "math-service-api" from the directory
- docker build -t math-service-api .


- To start the container and make the app available locally. -p 8000:8000 maps port 8000 in the container to port 8000 on the machine
- docker run -p 8000:8000 math-service-api


- A volume mount was used to prevent losing data between container runs
- docker run -p 8000:8000 -v $(pwd)/requests.db:/app/requests.db math-service-api

- 2 terminals windows were used

- 1st terminal to run the Docker container and view live FastAPI logs and error messages
- docker run -p 8000:8000 -v $(pwd)/requests.db:/app/requests.db math-service-api

- 2nd terminal to send API request, like curl and test the endpoints

- curl -X POST "http://localhost:8000/api/pow" -H "Content-Type: application/json" -d '{"a": 2, "b": 3}'


## Docker containerization: approach and steps
- To ensure portability, the project is Docker containerized. To facilitate run and deploy across environments.
- Base image: official Python slim image
- **Working directory**: /app
- **Dependencies**: copies requirements.txt and installs all packages
- **Source Code**: all project files merged to container
- **Expose Port**: 8000 for FastAPI access
- **Entrypoint**: Runs FastAPI by Uvicorn
- A .dockerignore file was created to prevent unnecessary files (Python cache, virtual environments, IDE settings from being 
included in the Docker build context, to keep the image smaller and builds cleaner

**In Docker**
- Instructions provided to run in a GitBash terminal


- 1.Build Image
- docker build -t math_service-api .


- 2.Run container
- docker run -d \
  --name math-service-api \
  -p 8000:8000 \
  -v "$(pwd)/requests.db:/app/requests.db" \
  math-service-api
- p 8000:8000 -> host -> container
- -v .../requests.db:... -> persist logs


- 3.Tests from host
- curl -X POST http://localhost:8000/api/factorial \
  -H "Content-Type: application/json" \
  -d '{"n":5}'


- 4.View docs
- http://localhost:8000/docs


## RabbitMQ Logging Integration
- Open a terminal in WSL or GitBash
- Run RabbitMQ in Docker to create the broker and management UI

- 1.Start broker
- docker run -d name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management


- 2.Wire
- Controllers now call publish_log(entry) after log_to_db
- A small consumer script (workers/rabbit_consumer.py) reads from the math logs exchange


- Open the management UI and on the http://localhost:15672 connect with guest credentials as user and password

- 3.Running
- Terminal 1: uvicorn math_service.app:app --reload
- Terminal 2: python math_service/workers/rabbit_consumer.py
- Terminal 3: send a request
- curl -X POST http://localhost:8000/api/fibonacci \
-H "Content-Type: application/json" \
-d '{"n":7}'

- curl -X POST http://localhost:8000/api/factorial \
  -H "Content-Type: application/json" \
  -d '{"n": 5}'


- Observe terminal 1: "Published fibonacci -> RabbitMQ"
- Observe terminal 2: JSON log output
- RabbitMQ UI(http://localhost:15672 -> Exchanges -> math_logs) displays message activity


## API-Key Authorization Integration
- To ensure only clients with a valid key may call /api/*:
- 1.Middleware inspects X-API-Key header on each request
- 2.In security.py, a check against a configured key(e.g: mathapikey47)
- 3.Requests missing or using the wrong key receive 401 Unauthorized

- Example:
- curl -X POST http://localhost:8000/api/pow \
  -H "X-API-Key: mathapikey47" \
  -H "Content-Type: application/json" \
  -d '{"a":3,"b":4}'

- return {"result":81}

- python -m uvicorn math_service.app:app
- Open docs http://127.0.0.1:8000/docs
- Check logs, open requests.db with DB Browser for SQLite (after server has stopped)

- Logging example: curl -X POST "http://127.0.0.1:8000/api/pow" -H "Content-Type: application/json" -d "{\"a\":2,\"b\":8}"
returns { "result": 256 } and logs the operation and result to requests.db in the requests_logs table.
