from fastapi.responses import JSONResponse

def success_response(message: str, data: dict = None):
    return JSONResponse(
        status_code=200,
        content={"message": message, "data": data or {}},
    )

def error_response(message: str, detail: str = None, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={"message": message, "detail": detail or ""},
    )
