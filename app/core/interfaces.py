from typing import TypedDict, Dict, Optional, List, Union, Literal

class AppRequiriments(TypedDict):
    memory_in_mb: int

class AppDescription(TypedDict):
    command: str
    setup_cmd: str
    env: Dict[str,str]
    repo: str
    name: str
    requirements: AppRequiriments

UnkownStatus = Literal["Unkown"]
RunningStatus = Literal["running"]
FailedStatus = Literal["failed"]
CompletedStatus = Literal["completed"]

AppStatus = Union[UnkownStatus, RunningStatus, FailedStatus, CompletedStatus]

class AppState(TypedDict):
      name: str
      pid: int
      return_code: Optional[int]
      started_at: str
      status: AppStatus

class NodeState(TypedDict):
    apps: Optional[List[AppState]]
    available_memory_in_mb: int
    battery_in_percent: int
    cpu_count: int 
    id: str 
    is_master: bool
