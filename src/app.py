from flask import Flask
from config import Figs, ENV_LOCAL_RUN
from figgy import FigService, ConfigWriter
import boto3
import logging
import os

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

app = Flask(__name__)

ssm = boto3.client('ssm', region_name='us-east-1')
svc = FigService(ssm)
FIGS = Figs(svc, lazy_load=True)

# Write & Update our current `figgy.json` file on every server run. This ensures our application & configs are in sync.
if os.environ.get(ENV_LOCAL_RUN) == "true":
    ConfigWriter().write(FIGS, destination_dir="figgy")


@app.route("/ok")
def ok():
    return "Ok!"


@app.route("/")
def hello():
    return f"Hello {FIGS.ADMIRED_PERSON}, {FIGS.SECRET_ADMIRER} is admiring you!"


@app.route("/db")
def db():
    return f"DB Connnection UL:  {FIGS.SQL_CONNECTION_STRING}"


if __name__ == "__main__":
    log.info("Starting app on http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=False)
