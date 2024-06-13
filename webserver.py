import json

import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sse_starlette.sse import EventSourceResponse
from starlette.middleware.cors import CORSMiddleware

import asyncio
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('command', type=str, help='The command to run and monitor')
args = parser.parse_args()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_event_stream_message(event_name, event_json):
    return (f'event: {event_name}\n'
            f'data: {event_json}\n\n')


async def waypoints_generator():
    waypoints = open('waypoints.json')
    waypoints = json.load(waypoints)
    for waypoint in waypoints[0: 10]:
        yield create_event_stream_message("locationUpdate", json.dumps(waypoint))


async def test_event_generator():
    for i in range(10):
        yield create_event_stream_message("testEvent", json.dumps({"id": i}))


@app.get("/test-stream")
async def test_stream():
    return StreamingResponse(test_event_generator(), media_type="text/event-stream")


def run_command(command):
    return subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('utf-8')


@app.get("/")
def run_command_and_display_output():
    return {"result": run_command(args.command)}


@app.get("/monitor", response_class=HTMLResponse)
def render_monitor_page(request: Request):
    return templates.TemplateResponse(request=request,
                                      name="monitor.html",
                                      context={"result": run_command(args.command)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
