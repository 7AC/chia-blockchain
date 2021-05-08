#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import re
import subprocess
import time

hostName = "localhost"
serverPort = 8080


class FarmServer(SimpleHTTPRequestHandler):

    statuses = {"Not available": 0,
                "Not synced or not connected to peers": 1,
                "Not running": 2,
                "Syncing": 3,
                "Farming": 4}

    strings = frozenset(["Total size of plots",
                         "Estimated network space",
                         "Expected time to win",
                         "Note"])

    def do_GET(self):
        self.send_response(200)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length"))
        body = self.rfile.read(content_length)
        body_json = json.loads(body)
        target = ""
        try:
            target = body_json["targets"]["target"]
        except (TypeError, KeyError):
            pass
        stdout = subprocess.check_output(["chia", "farm", "summary"])
        output = {}
        for line in stdout.decode("utf-8").split("\n"):
            try:
                name, value = line.split(": ")
                if not target or target == name:
                    output[name] = value
            except ValueError:
                continue
        stdout = subprocess.check_output(["plotman", "status"])
        tokens = re.split(" +", stdout.decode("utf-8"))
        output["Plotting"] = len([token for token in tokens if token == "32"])
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if self.path == '/search':
           self.wfile.write(bytes(json.dumps(list(output.keys())), "utf-8"))
        elif self.path == '/query':
           columns = []
           rows = []
           for name, value in output.items():
              column_type = "string" if name in self.strings else "number"
              column_value = value
              if name == "Farming status":
                  column_value = self.statuses[value]
              columns.append({"text": name, "type": column_type})
              rows.append(column_value)
           table = [{"columns": columns,
                     "rows": [rows],
                     "type": "table"}]
           self.wfile.write(bytes(json.dumps(table), "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), FarmServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
