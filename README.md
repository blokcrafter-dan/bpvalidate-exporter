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
```

## Usage

```
bpvalidate-export.py <options>
  options are:
    -p, --port=<export port> 
    -n, --network=<EOSIO chain> 
    -u, --uri=<source bp.json uri>
    -r, --refresh=<fetch refresh in seconds>
```

Note: you do not need to specify the URI, it will auto-set it based on the provided network parameter

## Defaults

```
PORT 8000
NETWORK eos
REFRESH 300
URI https://validate.eosnation.io/eos/bps.json
```

## Example Output

```
eosn_producer_active{chain="eos",owner="eosnationftw"} 1.0
eosn_producer_votes{chain="eos",owner="eosnationftw"} 6.01561876587203e+18
eosn_producer_unpaid_blocks{chain="eos",owner="eosnationftw"} 5556.0
eosn_producer_top21{chain="eos",owner="eosnationftw"} 1.0
eosn_producer_is_paid{chain="eos",owner="eosnationftw"} 1.0
eosn_producer_is_standby{chain="eos",owner="eosnationftw"} 0.0
eosn_producer_categories{category="api_endpoint",chain="eos",owner="eosnationftw"} 0.0
eosn_producer_categories{category="blacklist",chain="eos",owner="eosnationftw"} 0.0
eosn_producer_categories{category="bpjson",chain="eos",owner="eosnationftw"} 0.0
eosn_producer_categories{category="chains",chain="eos",owner="eosnationftw"} 0.0
eosn_producer_categories{category="general",chain="eos",owner="eosnationftw"} 1.0
eosn_producer_categories{category="history",chain="eos",owner="eosnationftw"} 5.0
eosn_producer_categories{category="hyperion",chain="eos",owner="eosnationftw"} 5.0
eosn_producer_categories{category="org",chain="eos",owner="eosnationftw"} 0.0
eosn_producer_categories{category="p2p_endpoint",chain="eos",owner="eosnationftw"} 0.0
eosn_producer_categories{category="regproducer",chain="eos",owner="eosnationftw"} 0.0
eosn_producer_categories{category="wallet",chain="eos",owner="eosnationftw"} 0.0
```
