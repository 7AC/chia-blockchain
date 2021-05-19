#!/bin/sh

for exporter in coinmarketcap-exporter plotman chia_exporter
do
   cd ../$exporter
   echo "exporting $exporter"
   ./start.sh
done
