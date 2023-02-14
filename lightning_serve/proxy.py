import asyncio
import pickle

from fastapi import Body, FastAPI, Request, Response

from lightning_serve.strategies.base import Strategy
from lightning_serve.utils import install_uvloop_event_loop

PROXY_ENDPOINT = "/api/v1/proxy"

app = FastAPI()
lock = asyncio.Lock()
proxy_metadata = None

with open("strategy.p", "rb") as f:
    strategy: Strategy = pickle.load(f)

# Instrumentator().instrument(app).expose(app)


@app.post(PROXY_ENDPOINT)
async def post_proxy(request: Request):
    global proxy_metadata
    local_proxy_metadata = await request.json()
    async with lock:
        proxy_metadata = local_proxy_metadata


@app.get(PROXY_ENDPOINT)
async def get_proxy(request: Request):
    global proxy_metadata
    async with lock:
        return proxy_metadata


def fn(request: Request, full_path: str, payload):
    global proxy_metadata

    if not proxy_metadata:
        resp = Response("The proxy_metadata is empty")
        resp.status_code = 404
        return resp

    response = strategy.make_request(request, full_path, proxy_metadata, payload)
    return response.json()


@app.post("/{full_path:path}")
def global_post(request: Request, full_path: str, payload: dict = Body(...)):
    return fn(request, full_path, payload)


@app.get("/{full_path:path}")
def global_get(request: Request, full_path: str):
    return fn(request, full_path, None)


if __name__ == "__main__":
    import argparse

    from uvicorn import run

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str)
    parser.add_argument("--port", type=int)
    hparams = parser.parse_args()

    install_uvloop_event_loop()

    run(
        app,
        host=hparams.host.replace("http://", "").replace("https://", ""),
        port=int(hparams.port),
    )
