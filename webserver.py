import json
import sys
import argparse
from subprocess import Popen, PIPE, CalledProcessError

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.middleware.cors import CORSMiddleware

parser = argparse.ArgumentParser()
parser.add_argument('command', type=str, help='The command to run and monitor')
args = parser.parse_args()

app = FastAPI()
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


def yield_command_output(command):
    with Popen(command, stdout=PIPE, bufsize=1, universal_newlines=True, shell=True) as p:
        for line in p.stdout:
            yield create_event_stream_message("testEvent", json.dumps({"output": line}))
            sys.stdout.flush()

    if p.returncode != 0:
        raise CalledProcessError(p.returncode, p.args)


@app.get("/monitor")
async def monitor():
    return StreamingResponse(yield_command_output(args.command), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
