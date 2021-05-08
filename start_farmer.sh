#!/bin/sh

cd /home/tac/chia-blockchain
. ./activate
chia start farmer
nohup python3 ./chia/server/start_http_server.py > http_server.log &
nohup python3 ./chia/server/start_exporter.py > exporter.log &
nohup python3 ./../coinmarketcap-exporter/coinmarketcap.py > coinmarketcap.log &
