#!/usr/bin/env python3
"""
    This exporter converts eosnation validation json.
"""

__author__      = "ghobson2013"
__created__     = ""
__revision__    = ""
__date__        = ""

import requests, json, time, os, sys, traceback, getopt
from prometheus_client.core import REGISTRY, GaugeMetricFamily
from prometheus_client import start_http_server

PORT=8000
NETWORK='eos'
REFRESH=300
VALIDATE_URL='https://validate.eosnation.io/eos/bps.json'
KIND_TYPES=['ok','info','skip','warn','err','crit']

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        try:
          bps = requests.get( url = VALIDATE_URL ).json()
          val_prod = len(bps['producers'])
          g = GaugeMetricFamily('eosn_producers', 'total producers', labels=['chain'])
          g.add_metric([NETWORK], val_prod)
          
          producer_active        = GaugeMetricFamily('eosn_producer_active', 'producer is_active', labels=['chain','owner'])
          producer_votes         = GaugeMetricFamily('eosn_producer_votes', 'producer votes', labels=['chain','owner'])
          producer_unpaid_blocks = GaugeMetricFamily('eosn_producer_unpaid_blocks', 'producer unpaid blocks', labels=['chain','owner'])
          producer_categories    = GaugeMetricFamily('eosn_producer_categories', 'producer message summary', labels=['chain','owner','category'])
          producer_top21         = GaugeMetricFamily('eosn_producer_top21', 'producer top 21 status' , labels=['chain','owner'])
          producer_is_paid       = GaugeMetricFamily('eosn_producer_is_paid', 'producer pay status', labels=['chain','owner'])
          producer_is_standby    = GaugeMetricFamily('eosn_producer_is_standby', 'producer is standby', labels=['chain','owner'])

          x=0
          while (x < val_prod):
            val_owner = bps['producers'][x]['regproducer']['owner']
            producer_active.add_metric([NETWORK,val_owner], float(bps['producers'][x]['regproducer']['is_active']))
            producer_votes.add_metric([NETWORK,val_owner], float(bps['producers'][x]['regproducer']['total_votes']))
            producer_unpaid_blocks.add_metric([NETWORK,val_owner], float(bps['producers'][x]['regproducer']['unpaid_blocks']))
            producer_top21.add_metric([NETWORK,val_owner], float(bps['producers'][x]['info']['is_top_21'])) 
            producer_is_paid.add_metric([NETWORK,val_owner], float( bps['producers'][x]['info']['is_paid']))
            producer_is_standby.add_metric([NETWORK,val_owner], float( bps['producers'][x]['info']['is_standby']))

            for val_cat in bps['producers'][x]['message_summary']:
              producer_categories.add_metric([NETWORK,val_owner,val_cat],KIND_TYPES.index(bps['producers'][x]['message_summary'][val_cat]))
            x+=1

          yield producer_active
          yield producer_votes
          yield producer_unpaid_blocks
          yield producer_top21
          yield producer_is_paid
          yield producer_is_standby
          yield producer_categories
          yield g
          yield GaugeMetricFamily('eosn_producer_up', 'eosn producer scrape success',1)
            
        except:
          traceback.print_exc()
          yield GaugeMetricFamily('eosn_producer_up', 'eosn producer scrape success',0)

if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:n:u:r:h", ["help", "port=", "network=","uri=","refresh="])
    except getopt.error as msg:
        print(msg)
        sys.exit("Invalid arguments.")

    for o, a in opts:
        if o in ("-h", "--help"):
          print("Usage: bpvalidate-export.py -p <export port> -n <EOSIO chain> -u <source bp.json uri> -r <fetch refresh in seconds>")
          sys.exit()

        if o in ("-p", "--port"):
          PORT=int(a)

        if o in ("-n", "--network"):
          NETWORK=str(a)
          VALIDATE_URL= "https://validate.eosnation.io/%s/bps.json"%NETWORK

        if o in ("-r", "--refresh"):
          REFRESH=int(a)

        if o in ("-u", "--uri"):
          VALIDATE_URL=str(a)

    print("Starting exporter on port %.0f for network %s , fetching every %.0fs from %s"%(PORT,NETWORK,REFRESH,VALIDATE_URL))
    start_http_server(PORT)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(REFRESH)
