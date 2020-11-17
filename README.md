# bpvalidate-exporter
Prometheus exporter to expose EOSNation's bpvalidate metrics

The exporter will read every 5 mins https://validate.eosnation.io/eos/bps.json and expose the relevant information as metrics
Configure prometheus with a new job and point the target at http://IP:8000 

The Ip address and portnumber can be changed in the python script

## Manual Installation

```
pip3 install -r requirements.txt
mkdir -p /usr/lib/systemd/system
cp bpvalidate-exporter.service /usr/lib/systemd/system
useradd prometheus
systemctl enable bpvalidate-exporter
systemctl start bpvalidate-exporter

## Usage

```
bpvalidate-export.py -p <export port> -n <EOSIO chain> -u <source bp.json uri> -r <fetch refresh in seconds>
```

Defaults are:
```
PORT 8000
NETWORK eos
REFRESH 300
URI https://validate.eosnation.io/eos/bps.json
```
