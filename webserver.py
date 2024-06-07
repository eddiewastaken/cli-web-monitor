import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('command', type=str, help='The command to run and monitor')
args = parser.parse_args()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


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
