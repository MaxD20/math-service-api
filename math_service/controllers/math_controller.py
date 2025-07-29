from fastapi import APIRouter, HTTPException
from math_service.schemas.math_schema import (
    PowerRequest, FactorialRequest, FibonacciRequest, MathResponse
)
from math_service.services.math_services import power, factorial, fibonacci


router = APIRouter()


@router.post("/pow", response_model=MathResponse)
async def compute_pow(data: PowerRequest):
    try:
        return MathResponse(result=power(data.a, data.b))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/factorial", response_model=MathResponse)
async def compute_factorial(data: FactorialRequest):
    try:
        return MathResponse(result=factorial(data.n))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/fibonacci", response_model=MathResponse)
async def compute_fibonacci(data: FibonacciRequest):
    try:
        return MathResponse(result=fibonacci(data.n))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
