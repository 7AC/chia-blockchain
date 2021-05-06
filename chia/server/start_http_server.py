import asyncio
from flask import Flask
from flask import jsonify
from chia.cmds.farm_funcs import summary

app = Flask("Chia HTTP Server")

# TODO: add options
rpc_port = None
wallet_rpc_port = None
harvester_rpc_port = None
farmer_rpc_port = None


@app.route('/api/farm/summary')
def api_farm_summary():
    data = asyncio.run(summary(rpc_port, wallet_rpc_port, harvester_rpc_port, farmer_rpc_port))
    return jsonify(data.to_json())


if __name__ == "__main__":
    app.run()
