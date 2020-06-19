import psutil
import time
import subprocess
import logging
import concurrent.futures

from flask import Flask
from datetime import datetime


class RougeSlaveException(Exception):
    """ Called when a slave has stopped responding but is not dead """


class ClusterProcess:
    def __init__(self, cmd,  id_):
        self._id = id_
        self._cmd = cmd
        self._proc = self.start()
        self._pid = self._proc.pid

    @property
    def pid(self):
        return self._pid

    @property
    def id(self) -> int:
        return self._id

    @property
    def proc(self) -> subprocess.Popen:
        return self._proc

    def logs(self):
        data = self._proc.stdout.readline().decode().replace('\n', '')
        print(data, end="")
        if data != '':
            return f"[{datetime.now().strftime('%D | %H:%M:%S')}][Cluster {self._id}] {data}"
        else:
            return None

    def restart(self):
        for i in range(3):
            logging.debug("Attempting restart in {}".format(3-i))
            time.sleep(1)
        logging.info("Cluster {}, Process with PID: {} is attempting to restart.".format(self.id, self.pid))
        try:
            self._proc.kill()
        except subprocess.SubprocessError:
            check = psutil.Process(self._proc.pid)
            if check.status() not in (psutil.STATUS_DEAD, psutil.STATUS_STOPPED):
                raise RougeSlaveException(
                    "Slave with PID {} has stopped responding but is not dead!".format(self._proc.pid))
        self._proc = self.start()
        logging.info("Cluster {}, Process with PID: {} has restarted successfully.".format(self.id, self.pid))
        return self

    def start(self) -> subprocess.Popen:
        logging.info("Cluster {} is attempting to start a new process.".format(self.id))
        return subprocess.Popen(self._cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


class SlaveManager:
    def __init__(self, target, shards, scale=1, name=__name__,
                 log_console=True, time_interval=0.2, keep_alive=True,
                 server_port=5000):
        if shards < scale:
            raise ValueError(
                "Amount of shards ({}) cannot be lower than the scale count ({})".format(shards, scale))
        self.name = name
        self.slaves = scale
        self.shards = shards
        self.log_console = log_console
        self.target = target
        self.time_interval = time_interval
        self.keep_alive = keep_alive
        self.server_port = server_port

        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.app = Flask(name)
        self.clusters = {}
        self.running = True

    def __enter__(self, scale=1, name=__name__):
        self.name = name
        self.slaves = scale
        self.thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown_slaves()
        self.thread_pool.shutdown()

    def shutdown_slaves(self):
        self.running = False
        for id_, proc in self.clusters.items():
            proc: ClusterProcess = proc
            proc.proc.kill()

    def run(self):
        self.thread_pool.submit(self.app.run, "0.0.0.0", **{'port': self.server_port})
        self.generate_slaves()

    def generate_slaves(self):
        shards, remaining = divmod(self.shards, self.slaves)
        while remaining != 0:
            self.shards += 1
            shards, remaining = divmod(self.shards, self.slaves)
        for i in range(self.slaves):
            cmd = f"""python "{self.target}" {i} {shards} {self.shards}"""
            self.clusters[i] = ClusterProcess(cmd=cmd, id_=i)
            print(f"Slave {i+1}/{self.slaves}  | Starting Slave {i}, PID: {self.clusters[i].pid}")
        self.handle_logs()

    def handle_logs(self):
        while self.running:
            for id_, proc in self.clusters.items():
                try:
                    util_check = psutil.Process(pid=proc.proc.pid)
                    with util_check.oneshot():
                        status = util_check.status()
                    if status == psutil.STATUS_RUNNING:
                        content = proc.logs()
                        if content is not None:
                            self.on_console_log(proc, content)
                    else:
                        self.on_slave_dead(proc)
                except psutil.NoSuchProcess:
                    self.on_slave_dead(proc)
            time.sleep(self.time_interval)

    def on_slave_dead(self, slave: ClusterProcess):
        if self.keep_alive:
            self.clusters[slave.id] = slave.restart()

    def on_console_log(self, slave, content):
        pass





