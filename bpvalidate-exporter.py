#!/usr/bin/env python
"""
    This exporter converts eosnation validation json.
"""

__author__      = "ghobson2013"
__created__     = ""
__revision__    = ""
__date__        = ""

import requests, json, time, os, sys, traceback
from prometheus_client.core import REGISTRY, GaugeMetricFamily
from prometheus_client import start_http_server

EOSN_VALIDATE_URL='https://validate.eosnation.io/eos/bps.json'
EOSN_INTERNAL='https://validate.eosnation.io/eos/producers/eosnationftw.json'
KIND_TYPES=['ok','info','skip','warn','err','crit']

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        try:
          bps = requests.get( url = EOSN_VALIDATE_URL ).json()
          val_prod = len(bps['producers'])
          g = GaugeMetricFamily("eosn_producers", 'total producers', labels=['chain'])
          g.add_metric(["EOS"], val_prod)
          
          producer_active = GaugeMetricFamily("eosn_producer_active", 'producer is_active', labels=['chain','owner'])
          producer_votes  = GaugeMetricFamily("eosn_producer_votes", 'producer votes', labels=['chain','owner'])
          producer_unpaid_blocks = GaugeMetricFamily("eosn_producer_unpaid_blocks", 'producer unpaid blocks', labels=['chain','owner'])
          producer_categories = GaugeMetricFamily("eosn_producer_categories", 'producer message summary', labels=['chain','owner','category'])
          x=0
          while (x < val_prod):
            val_owner = bps['producers'][x]['regproducer']['owner']
            producer_active.add_metric(['EOS',val_owner], float(bps['producers'][x]['regproducer']['is_active']))
            producer_votes.add_metric(['EOS',val_owner], float(bps['producers'][x]['regproducer']['total_votes']))
            producer_unpaid_blocks.add_metric(['EOS',val_owner], float(bps['producers'][x]['regproducer']['unpaid_blocks']))
            
            for val_cat in bps['producers'][x]['message_summary']:
              producer_categories.add_metric(['EOS',val_owner,val_cat],KIND_TYPES.index(bps['producers'][x]['message_summary'][val_cat]))
            x+=1

          yield producer_active
          yield producer_votes
          yield producer_unpaid_blocks
          yield producer_categories
          yield g
            
        except:
          traceback.print_exc()


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(300)
