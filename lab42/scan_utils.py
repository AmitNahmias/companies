import multiprocessing
from typing import List, Optional
from dataclasses import dataclass, field

RESULTS_QUEUE, REQUESTS_QUEUE = multiprocessing.Queue(), multiprocessing.Queue()


@dataclass
class ScanRequest:
    """
    Define ScanRequest data.
    """
    id: int  # same as in the request ipv4: str ports: List[int]
    ipv4: str
    ports: List[int]


@dataclass
class PortResult:
    """
    Define PortResult data.
    """
    port: int
    is_open: bool
    is_http: Optional[bool]

    def __str__(self) -> str:
        """
        Represent port result as string.

        :return: Port result as string.
        """
        return f'Port {self.port} is open: ' \
               f'{self.is_open}, is http: {self.is_http} '


@dataclass
class ScanResult:
    """
    Define ScanResult data.
    """
    id: int = None
    ipv4: str = None
    is_alive: bool = False
    ports: List[PortResult] = field(default_factory=list)

    def __str__(self) -> str:
        """
        Represent scan result as string.

        :return: Scan result as string.
        """
        self.output = '=============================================='
        self.output += f'\nHost {self.ipv4} is alive: {self.is_alive}'
        for port in self.ports:
            self.output += "\n" + str(port)
        self.output += '\n=============================================='
        return self.output


def create_requests() -> None:
    """
    For testing scanner
    """
    ports = [1, 22, 53, 80, 443, 8080, 8443]
    ips = ['2.2.2.2', '8.8.8.8', '8.8.4.4', '1.1.1.1',
           '127.0.0.1', '142.251.33.206']
    for i in range(len(ips)):
        REQUESTS_QUEUE.put(ScanRequest(id=i, ipv4=ips[i], ports=ports))
