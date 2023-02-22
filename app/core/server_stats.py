from .interfaces import NodeState
import subprocess, os


class ServerStats():
    is_master: bool
    id: str
    memory_fallback_value: int
    
    def __init__(self, id: str, is_master: bool, memory_fallback=int) -> None:
        # gives a single float value
        self.is_master = is_master
        self.id = id
        self.memory_fallback_value = memory_fallback
        self.load_statistics()

    def _try_get_batery_percent(self) -> int:
        # TODO
        return 0
    
    def get_number_of_cpus(self) -> int:
        cpus = os.cpu_count()
        return cpus if cpus else 0
        
    def get_avaliable_memory(self) -> int:
        try:
            res = subprocess.run(["cat", "/proc/meminfo"], capture_output=True, text=True)
            if res.stdout:
                memory_info = list(map(lambda v: v.split(),  filter(bool, res.stdout)))
                print(memory_info)

                for key, value, _ in memory_info:
                    if key == 'MemAvailable:':
                        return int(int(value) / 1000)

            return self.memory_fallback_value
        except:
            return self.memory_fallback_value

    def load_statistics(self) -> None:
        self.cpu_count = self.get_number_of_cpus()
        self.available_memory_in_mb = self.get_avaliable_memory()
        self.battery_percent = self._try_get_batery_percent()

    def asdict(self) -> NodeState:
        self.load_statistics()
        return {
            "id": self.id,
            "apps": [],
            "is_master": self.is_master,
            "cpu_count": self.cpu_count,
            "available_memory_in_mb": self.available_memory_in_mb,
            "battery_in_percent": self.battery_percent,
        }