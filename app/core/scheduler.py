from typing import List, Optional

from .client import MACClient
from .server_stats import ServerStats
from .app import App
from .interfaces import AppDescription, AppState, NodeState

class Scheduler:
    apps: List[App] = []
    mac_client: MACClient
    node_name: str
    server_stats: ServerStats
    
    def __init__(self, mach_client: MACClient, server_stats: ServerStats, node_name: str) -> None:
        self.mac_client = mach_client
        self.server_stats = server_stats
        self.node_name = node_name

    def get_cluster_statistics(self) -> List[NodeState]:
        server_stat = self.server_stats.asdict()
        server_stat["apps"] = list(map(lambda app: app.asdict(), self.apps))

        response: List[NodeState] = []
        response.append(server_stat)

        workers_stats_responses = self.mac_client.get_workers_statistics()
        for worker_node_response in workers_stats_responses:
            response.append(worker_node_response) 
        return response
    
    def stop(self, name: str) -> List[AppState]:
        procs: List[AppState] = []
        for app in self.apps:
            if str(app.asdict()["name"]) == name:
                print("stoping proccess", name)
                app.stop()
                procs.append(app.asdict())

        remote_procs = self.mac_client.stop_proccess(name)
        return procs + remote_procs
    
    def select_node_by_requirements(self, app: AppDescription) -> NodeState:
        required_mem_in_mb = app["requirements"]["memory_in_mb"]
        nodes = self.get_cluster_statistics()

        selected_node = None
        for node in nodes:
            if required_mem_in_mb <= node["available_memory_in_mb"]:
                selected_node = node
                break
        
        if not selected_node:
            raise Exception("no node able to requirements")
        
        return selected_node
    

    def schedule(self, requirements) -> AppState:

        node = self.select_node_by_requirements(requirements)
        # print(node)
        if node["id"] == self.node_name:
            name = requirements["name"]
            repo = requirements["repo"]
            command  = requirements["command"]
            environments = requirements["env"]
            setup_cmd = requirements["setup_cmd"]

            process = App(
                name=name, 
                repo=repo, 
                setup_cmd=setup_cmd, 
                envs=environments, 
                cmd=command
            )

            process.start()
            self.apps.append(process)

            return process.asdict()
        else:
            return self.mac_client.start(requirements)
    
