#!/usr/bin/python

import time
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import requests
import subprocess


# TODO: parametrize
CHIA_HTTP_SERVER = "http://localhost:5000/api/farm/summary"


class ChiaCollector:

    farm_status = {"Not available": 0,
                   "Not synced or not connected to peers": 1,
                   "Not running": 2,
                   "Syncing": 3,
                   "Farming": 4}

    def __init__(self, target):
        self.target = target

    def get(self):
        response = requests.get(self.target)
        return response.json()

    def collect(self):
        data = self.get()
        for name, value in data.items():
            if name == "status":
                value = self.farm_status[value]
            yield GaugeMetricFamily(f"chia_farm_summary_{name}", f"chia_farm_summary_{name}", value=value)
            #stdout = subprocess.check_output(["plotman", "status"]).decode("utf-8")
            #yield GaugeMetricFamily("chia_farm_summary_plots_in_progress", "plotman_jobs_count", value=stdout.count("/mnt/plotter"))


if __name__ == "__main__":
    start_http_server(8000)
    REGISTRY.register(ChiaCollector(CHIA_HTTP_SERVER))
    while True:
        time.sleep(1)
