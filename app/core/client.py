import requests
from typing import List, Optional
from .interfaces import NodeState, AppState

class MACClient:
    hosts: List[str]

    def __init__(self, hosts) -> None:
        self.hosts = hosts

    def _get_single_worker_statistics(self, host) -> List[NodeState]:
        return requests.get(host).json()

    def get_workers_statistics(self) -> List[NodeState]:
        nodes: List[NodeState] = []
        for host in self.hosts:
            workers_states = self._get_single_worker_statistics(host)
            for state in workers_states:
                nodes.append(state)
        return nodes
    
    def _stop_proccess_in_single_host(self, host, name) -> AppState:
        resp = requests.get(f"{host}/process/{name}/stop")
        return resp.json()

    def stop_proccess(self, name) -> List[AppState]:
        procs: List[AppState] = []
        for host in self.hosts:
            response = self._stop_proccess_in_single_host(host, name)
            if response.get("Status", None) != "not found":
                procs.append(response)

        return procs

    def _start_in_single_host(self, host, req) -> AppState:
        return requests.post(host, json=req).json()
    
    def start(self, req) -> AppState:
        for host in self.hosts:
            resp = self._start_in_single_host(host, req)
            return resp
        
        raise Exception("app can't start")

        