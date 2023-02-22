
import os 
from flask import Flask,request
from uuid import uuid4
from core import App, ServerStats, MACClient, Scheduler, NodeState, AppState
from typing import List, Union, TypedDict, Literal
import psutil
host = os.getenv("HOST", '')
port = int(os.getenv("PORT", '8000'))
raw_hosts = os.getenv("WORKERS", '')

workers_hosts = []
if raw_hosts != "":
    workers_hosts = raw_hosts.split(",")

print(workers_hosts)
instance_id = uuid4()

node_name = f"mac-{instance_id}"
is_master = False

if len(workers_hosts) > 0:
    is_master = True

app = Flask(node_name)


server_stats = ServerStats(node_name, is_master)
mac_client = MACClient(workers_hosts)

scheduler = Scheduler(
    server_stats=server_stats,
    mach_client=mac_client,
    node_name=node_name,
)

class NotFoundResponse(TypedDict):
    status: Literal["not found"]

AppActionResponse = Union[AppState, NotFoundResponse]

@app.route('/', methods = ['GET'])
def server_statistics() -> List[NodeState]:
    return scheduler.get_cluster_statistics()

@app.route('/app/<name>/stop', methods = ['POST'])
def stop_app(name) -> List[AppState]:
    return scheduler.stop(name)

@app.route('/', methods = ['POST'])
def start_app() -> AppState:
    message = request.json
    return scheduler.schedule(message)

if __name__ == '__main__':
   app.run(host = host, port = port, debug = False)
