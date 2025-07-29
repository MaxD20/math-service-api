from fastapi import FastAPI


from math_service.controllers import math_controller


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Math API is running"}


app.include_router(math_controller.router, prefix="/api")
