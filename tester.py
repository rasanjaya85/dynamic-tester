#!/usr/bin/env python

from pprint import pprint
import time
import datetime
import json
from zapv2 import ZAPv2
from elasticsearch import Elasticsearch

input_target = 'http://localhost:8080/'
# zap = ZAPv2()
#
# zap = ZAPv2(proxies={'http':'http://127.0.0.1:8090'})
#
# print "Accessing the Target %s " % target
# zap.urlopen(target)
# time.sleep(2)
API_KEY = 'pto8gko6c8gm4imnmf2ort31ef'

zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090'})
zap.urlopen(input_target)
time.sleep(2)

# print 'Spidering target %s' % input_target
# scanid = zap.spider.scan(input_target, apikey = API_KEY)
# print 'Scanid is: %s' % scanid

print 'Spidering target %s' % input_target
scanID = zap.spider.scan(input_target, apikey=API_KEY)


# Progress of spider
time.sleep(2)
while (int(zap.spider.status(scanID)) < 100):
    print 'Spider progress %s%% ' % zap.spider.status(scanID)
    time.sleep(2)

print 'Spider scan has completed'
time.sleep(5)

print 'Active scan has started on %s' % input_target
scanID = zap.ascan.scan(input_target, apikey = API_KEY)


while(int(zap.ascan.status(scanID)) < 100):
    print 'Active scanning progress %s%%' % zap.ascan.status(scanID)
    time.sleep(5)

print 'Dynamic Scan has completed'

# Report the results
print 'Hosts: ' + ', '.join(zap.core.hosts)
print 'Alerts: '
pprint(zap.core.alerts())

print 'Dynamic Scan report as completed'

#Send to elasticsearh

scanjson = {}
scanjson["zapscanid"] = scanID
scanjson["date"] = str(datetime.datetime.now())
scanjson["url"] = input_target
scanjson["alerts"] = zap.core.alerts()

es = Elasticsearch()
es.index(index='scans', doc_type='scan',  body=json.dumps(scanjson))
zap.core.shutdown()

print "scan ID is %s" % scanID
print "scanned data object %s" % scanjson
