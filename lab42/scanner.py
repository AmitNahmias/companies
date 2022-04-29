import multiprocessing
import subprocess
import requests
import socket
import platform

from lab42.logger import setup_logger
from lab42.scan_utils import ScanRequest, ScanResult, PortResult, \
    create_requests, REQUESTS_QUEUE, RESULTS_QUEUE

ICMP_PACKETS_TO_SEND = '1'  # as string, sends only one to reduce time
PING_REQUEST_TIMEOUT = 5  # in seconds
SOCKET_TIMEOUT = 3  # in seconds
SUCCESS_RETURN_CODE = 0
HTTP_FORMAT = 'http://{host_ip}:{host_port}/'
HTTPS_FORMAT = 'https://{host_ip}:{host_port}/'
PING_COMMAND = 'ping'
PING_COUNT_FLAG = {'Linux': '-c', 'Windows': '-n'}


class Scanner:
    def __init__(self, host: ScanRequest, scanner_id: int):
        """
        Define scanner.

        param host: Host to scan.
        param scanner_id: Scanner id, used for logger.
        """
        self._id = scanner_id
        self._host = host
        self._scan_result = ScanResult()
        self._logger = setup_logger(logger_id=self._id)

    def _check_current_os(self) -> str:
        """
        Check os on node.

        :return: OS type.
        """
        self._logger.info(f'I am running on {platform.system()}')
        return platform.system()

    @staticmethod
    def _create_port_result(port: int, is_http: bool = False,
                            is_open: bool = False) -> PortResult:
        """
        Initiate PortResult instance.

        param port: Port number.
        param is_http: Is the port is port of http service.
        param is_open: Is the port is listening

        :return: New PortResult instance filled in input values.
        """
        return PortResult(port=port, is_open=is_open, is_http=is_http)

    def _check_http_listen(self, host_ip: str, port: int) -> bool:
        """
        Check if port's service is http/s and returns appropriate boolean value.

        param host_ip: Host ip to check.
        param port: Host port to check.

        :return: True if http/s.
        """

        response = None
        try:
            # Check for https connection.
            self._logger.info(
                f'Trying HTTPS connection to {host_ip} in port {port}.')
            response = requests.get(
                HTTPS_FORMAT.format(host_ip=host_ip, host_port=port))
        except Exception:
            try:
                self._logger.info(
                    f'HTTPS connection to {host_ip} in port {port} failed.')
                self._logger.info(
                    f'Trying HTTP connection to {host_ip} in port {port}.')
                # Check for http connection if there is no https.
                response = requests.get(
                    HTTP_FORMAT.format(host_ip=host_ip, host_port=port))
            except Exception:
                self._logger.info(
                    f'HTTP connection to {host_ip} in port {port} failed.')
                return False
        return response.ok

    def _check_if_host_is_alive(self, host_ip: str) -> None:
        """
        Check if host is alive using ping command.

        param host_ip: Host ip.
        """

        self._scan_result.ipv4 = host_ip
        ping_count_flag = PING_COUNT_FLAG[self._check_current_os()]
        ping_cmd = [PING_COMMAND, ping_count_flag, ICMP_PACKETS_TO_SEND,
                    host_ip]
        self._logger.info(f'Pinging to {host_ip}.')
        if subprocess.call(ping_cmd, timeout=PING_REQUEST_TIMEOUT,
                           stdout=subprocess.DEVNULL) == SUCCESS_RETURN_CODE:
            self._logger.info(
                f'Pinging to {host_ip} succeeded, {host_ip} is alive.')
            self._scan_result.is_alive = True
        else:
            self._logger.info(
                f'Pinging to {host_ip} failed, {host_ip} is dead.')
            self._scan_result.is_alive = False

    def _check_if_port_is_open(self, host_ip: str, port: int) -> None:
        """
        Check if port is listening and write result to scan result.

        param host_ip: Host ip to check.
        param port: Host port to check.
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(SOCKET_TIMEOUT)
            response = s.connect_ex((host_ip, port))
        if response == SUCCESS_RETURN_CODE:
            self._logger.info(f'{host_ip} listening in port {port}.')
            is_web_service = self._check_http_listen(host_ip=host_ip, port=port)
            result = self._create_port_result(port=port, is_http=is_web_service,
                                              is_open=True)
        else:
            self._logger.info(f'{host_ip} not listening in port {port}.')
            result = self._create_port_result(port=port)
        self._scan_result.ports.append(result)

    def _check_host_ports(self, host_ip: str, ports_to_scan: list) -> None:
        """
        Scan all hosts port and write appropriate result.

        param host_ip: Host ip to check.
        param ports_to_scan: Port list to scan on host.
        """

        for port in ports_to_scan:
            self._logger.info(
                f'Checking connection to {host_ip} in port {port}.')
            self._check_if_port_is_open(host_ip=host_ip, port=port)

    def run(self) -> ScanResult:
        """
        Run single scan.

        :return: Scan result.
        """
        host_ip = self._host.ipv4
        self._scan_result.id = self._host.id
        self._logger.info(f'Start checking {host_ip}')
        self._check_if_host_is_alive(host_ip=host_ip)

        # To ensure that I'm not wasting  time on scanning "dead" host
        if self._scan_result.is_alive:
            self._check_host_ports(host_ip=host_ip,
                                   ports_to_scan=self._host.ports)

        self._logger.info(f'Done checking {host_ip}')
        return self._scan_result


def start(request_queue: multiprocessing.Queue,
          responses_queue: multiprocessing.Queue, scanner_id: int) -> None:
    """
    Control the flow of scanner.

    :param request_queue: Queue that contains ScanRequests.
    :param responses_queue: Queue to contain ScanResults.
    :param scanner_id: Scanner's id number.
    """
    try:
        while True:
            host: ScanRequest = request_queue.get()
            scanner = Scanner(host=host, scanner_id=scanner_id)
            result = scanner.run()
            # print(result)  # If you want to print each result
            responses_queue.put(obj=result)
    except KeyboardInterrupt:
        print('Done for today :)')


def main() -> None:
    """
    Control the flow of the program 
    """

    cores = multiprocessing.cpu_count()  # Get the number of cores in the node
    processes = []
    create_requests()  # Create requests for testing

    # Create processes
    for core in range(cores):
        process = multiprocessing.Process(target=start, args=(
            REQUESTS_QUEUE, RESULTS_QUEUE, core))
        processes.append(process)
        process.start()


if __name__ == '__main__':
    main()
