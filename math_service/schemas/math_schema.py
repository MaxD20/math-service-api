from pydantic import BaseModel, Field


class PowerRequest(BaseModel):
    a: int = Field(..., ge=0)
    b: int = Field(..., ge=0)


class FactorialRequest(BaseModel):
    n: int = Field(..., ge=0)


class FibonacciRequest(BaseModel):
    n: int = Field(..., ge=0)


class MathResponse(BaseModel):
    result: int
