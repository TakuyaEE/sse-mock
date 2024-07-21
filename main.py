import asyncio
import json

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from dummy_data import streaming_dummy_data, blocking_dummy_data
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
    for item in streaming_dummy_data:
        await asyncio.sleep(item["duration"])
        yield f"data:{json.dumps(item["data"])}\n\n"
    yield f"data: [DONE]\n\n"


@app.post("/v1/workflows/run")
async def workflow(body: RequestBody):
    if body.response_mode == "blocking":
        return json.dumps(blocking_dummy_data)
    else:
        return StreamingResponse(
            content=return_dummy_stream(), media_type="text/event-stream"
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
