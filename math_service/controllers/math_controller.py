# Maxim Dragos, Data Engineer

from fastapi import APIRouter, HTTPException
from math_service.schemas.math_schema import (
    PowerRequest, FactorialRequest, FibonacciRequest, MathResponse
)
from math_service.services.math_services import power, factorial, fibonacci
from math_service.models.request_log_model import log_to_db
from math_service.schemas.log_schema import LogEntry

print(">>> math_controller.py loaded!")
router = APIRouter()


@router.post("/pow", response_model=MathResponse)
async def compute_pow(data: PowerRequest):
    print(">>>> /api/pow CALLED with", data)
    try:
        result = power(data.a, data.b)
        entry = LogEntry(
            operation="pow",
            input_data=data.model_dump(),
            result=str(result),
            status_code=200
        )
        log_to_db(entry)
        return MathResponse(result=result)
    except Exception as e:
        entry = LogEntry(
            operation="pow",
            input_data=data.model_dump(),
            result=str(),
            status_code=400
        )
        log_to_db(entry)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/factorial", response_model=MathResponse)
async def compute_factorial(data: FactorialRequest):
    try:
        result = factorial(data.n)
        entry = LogEntry(
            operation="factorial",
            input_data=data.model_dump(),
            result=str(result),
            status_code=200
        )
        log_to_db(entry)
        return MathResponse(result=result)
    except Exception as e:
        entry = LogEntry(
            operation="factorial",
            input_data=data.model_dump(),
            result=str(e),
            status_code=400
        )
        log_to_db(entry)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fibonacci", response_model=MathResponse)
async def compute_fibonacci(data: FibonacciRequest):
    try:
        result = fibonacci(data.n)
        entry = LogEntry(
            operation="fibonacci",
            input_data=data.model_dump(),
            result=str(result),
            status_code=200
        )
        log_to_db(entry)
        return MathResponse(result=result)
    except Exception as e:
        entry = LogEntry(
            operation="fibonacci",
            input_data=data.model_dump(),
            result=str(e),
            status_code=400
        )
        log_to_db(entry)
        raise HTTPException(status_code=400, detail=str(e))
