# Maxim Dragos, Data Engineer

from pydantic import BaseModel


class LogEntry(BaseModel):
    operation: str
    input_data: dict
    result: str
    status_code: int
