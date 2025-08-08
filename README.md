# Math Microservice API

Maxim Dragos, Data Engineer

- A FastAPI that uses a microservice for computing mathematical operations, such as: 
power, factorial, Fibonacci with request/response logging to an SQLite database. 

- The API utilize Pydantic models, supports in memory caching, and provides an interactive Swagger UI. The program was developed using MVCS principles.

## Features perspective

- The endpoints used are:

- POST /api/pow that compute a^b

- POST /api/factorial that compute factorial of n

- POST /api/fibonacci that compute n-th Fibonacci number

Every API call is logged in requests.db (requests_logs table) with operation, input, result and status code.

For the interactive Docs, it used browse and test endpoints at /docs(Swagger UI)
- Backend: FastAPI application(app.py)
- Database: SQLite (requests.db in project root)
- Logging: Each successful or failed request is stored by log_to_db in request_log_model.py
- Caching: In memory cache avoid recomputation for repeated requests

## Architecture breakdown:
- The models(mth_service/models/): contains request_log_model.py that handles database table initialization and provide the log_to_db
function to record each API request and response in the requests_logs table of SQLite.

- Views(app.py) initializes the FastAPI application, includes the main API router, and exposes a health check endpoint(/)

- Controllers(math_service/controllers/): math_controller.py defines all API endpoints (/api/pow, /api/factorial, /api/fibonacci) orchestrates
input validation, error handling, result construction and logging via Models.

- Services(math_service/services/): contains business logic for mathematical operations(power, factorial, Fibonacci), and integrates a simple
in memory caching layer for performance

- Schemas (math_service/schemas/): math_schema.py defines request/response Pydantic models for strict validation, log_schema.py is a pydantic model for a log entry, used by both controller and the logging model.

## Working principle
- **Client** sends a request to an endpoint (/api/pow) by Swagger UI, curl, or HTTP client.
- **Controller** (math_controller.py) receives the request, validates the input using Pydantic schemas.
- **Service** (math_services.py) computes the result, using cache.
- **Controller** logs each request(inputs, result, status code) by calling log_to_db from Model (reques_log_model.py)
- **View** (app.py) ties everything together and provides a root check.

## Content
- app.py -> app entrypoint(view)
- requests.db -> SQLite database
- math_controller.py -> API endpoints (controller)
- request_log_model,py -> Database logic (model)
- math_schema.py -> API input/output model(schema)
- log_schema.py -> log entry model (schema)
- math_services.py -> bussiness logic and caching (service)
- sqlite_view.py -> connects SQLite database and prints out both the list of tables and all rows from the requests_logs table.
- test_math_service.py -> This script contains unit tests for the mathematical business logic in the Service layer (math_services.py)

## Run the server:
- python -m uvicorn math_service.app:app
- Open docs http://127.0.0.1:8000/docs
- Check logs, open requests.db with SQLite Viewer Web App (after server has stopped)

- Logging example: curl -X POST "http://127.0.0.1:8000/api/pow" -H "Content-Type: application/json" -d "{\"a\":2,\"b\":8}"
returns { "result": 256 } and logs the operation and result to requests.db in the requests_logs table.



