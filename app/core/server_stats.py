import psutil
from .interfaces import NodeState

class ServerStats():
    is_master: bool
    id: str
    
    def __init__(self, id: str, is_master: bool) -> None:
        # gives a single float value
        self.is_master = is_master
        self.id = id
        self.load_statistics()

    def _try_get_batery_percent(self) -> int:
        try:
            battery = psutil.sensors_battery()
            return battery.percent or 0
        except:
            return 0
    
    def load_statistics(self) -> None:
        # gives a single float value
        self.cpu = psutil.cpu_percent(interval=0.25)
        self.cpu_count = psutil.cpu_count()
        self.physical_cpu = psutil.cpu_count(logical=False)
        self.virtual_memory = psutil.virtual_memory()
        self.available_memory_in_mb = int(self.virtual_memory.available / 1048576)
        self.battery_percent = self._try_get_batery_percent()

    def asdict(self) -> NodeState:
        self.load_statistics()
        return {
            "id": self.id,
            "apps": [],
            "is_master": self.is_master,
            "cpu_percent": self.cpu,
            "physical_cpu": self.physical_cpu,
            "cpu_count": self.cpu_count,
            "available_memory_in_mb": self.available_memory_in_mb,
            "battery_in_percent": self.battery_percent,
        }