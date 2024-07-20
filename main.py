import asyncio
import json

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def handler(request: Request, exc: RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class RequestBody(BaseModel):
    inputs: str
    response_mode: str
    user: str


async def return_dummy_stream():
    dummy_response = [
        {"streaming": "replace here 1"},
        {"streaming": "replace here 2"},
        {"streaming": "replace here 3"},
        {"streaming": "replace here 4"},
        {"streaming": "replace here 5"},
        {"streaming": "replace here 6"},
        {"streaming": "replace here 7"},
        {"streaming": "replace here 8"},
        {"streaming": "replace here 9"},
    ]
    for item in dummy_response:
        await asyncio.sleep(1.0)
        yield f"data:{json.dumps(item)}\n\n"
    yield f"data: [DONE]\n\n"


@app.post("/v1/workflows/run")
async def workflow(body: RequestBody):
    if body.response_mode == "blocking":
        return json.dumps({"blocking": "replace here"})
    else:
        return StreamingResponse(
            content=return_dummy_stream(), media_type="text/event-stream"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
