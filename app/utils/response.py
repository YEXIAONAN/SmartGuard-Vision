from datetime import datetime


def success_response(data, message: str = "success", code: int = 0):
    return {
        "code": code,
        "message": message,
        "data": data,
        "timestamp": datetime.now(),
    }
