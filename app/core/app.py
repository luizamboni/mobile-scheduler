import datetime, subprocess
from .interfaces import AppState, AppStatus
from typing import cast, Dict
from uuid import uuid4

class App:
    name: str
    cmd: str
    repo: str
    envs: Dict[str, str]
    setup_cmd: str
    def __init__(self, name, repo, setup_cmd, envs, cmd) -> None:
        self.stated_at = datetime.datetime.now()
        self.name = name
        self.cmd = cmd
        self.envs = envs
        self.repo = repo
        self.setup_cmd = setup_cmd
        self.uuid = uuid4()
        self.setup()

    def setup(self) -> None:
        dir = f"./apps/{self.name}/{self.uuid}"
        _setup = f"""
rm -rf {dir}
git clone {self.repo} {dir}
cd {dir}
{self.setup_cmd}
        """
        subprocess.Popen(_setup, shell=True)

    def start(self) -> AppState:
        cmd = "exec "
        for key, value in self.envs.items():
            cmd += f"{key}='{value}' "
        cmd += self.cmd
        self.proccess = subprocess.Popen(cmd, shell=True)
        return self.asdict()

    def _status(self) -> AppStatus:
        status = "Unkown"
        returned_code = self.proccess.returncode

        if not returned_code:
            status = "running"
        elif returned_code < 0:
            status = "faild"
        else:
            status = "completed"

        return cast(AppStatus, status)


    def stop(self) -> AppState:
        if self._status() == "running":
            proc = self.proccess
            try:
                outs, errs = proc.communicate(timeout=15)
            except subprocess.TimeoutExpired:
                proc.kill()
                outs, errs = proc.communicate()
        return self.asdict()
            

    def asdict(self) -> AppState:
        status = self._status()
        returned_code = self.proccess.returncode
    
        return {
            "name": self.name,
            "pid": self.proccess.pid,
            "status": status,
            "return_code": returned_code,
            "started_at": self.stated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
