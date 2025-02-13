from fastapi.responses import JSONResponse

def success_response(message: str, data: dict = None, status_code: int = 200):
    response = {"status": "success", "message": message}
    if data:
        response["data"] = data
    return JSONResponse(status_code=status_code, content=response)

def error_response(message: str, status_code: int = 400):
    return JSONResponse(status_code=status_code, content={"status": "error", "message": message})
