import diamond.collector
import json
#import simplejson as json
import urllib2
from urlparse import urlparse
import base64

# Default strategy it to use json (good enough on python2.7). simplejson can be faster if updated. ymmv
try:
  import json
except ImportError:
  import simplejson as json
except ImportError:
  log.info("ERROR: json or simplejson python module, required by the CouchBaseCollector does not exist in your python environment")

class CouchBaseCollector(diamond.collector.Collector):

  def get_default_config(self):
    config = super(CouchBaseCollector, self).get_default_config()
    config.update({
      'host':        'localhost',
      'port':        8091,
      'path':        'beer-sample',
      'username': 'Administrator',
      'password': 'changeme'
    })
    return config


  def collect(self):
    self.log.info("Starting to collect!")
    self.log.info("collecting from host: " + self.config['host'] + " port: " + str(self.config['port']))

    url = 'http://localhost:8091/pools/default/buckets/' + self.config['path']
    self.log.info("URL: " + url)

    base64string = base64.encodestring('%s:%s' % (self.config['username'], self.config['password'])).replace('\n', '')
    request = urllib2.Request(url);
    request.add_header("Authorization", "Basic %s" % base64string)

    try:
      f = urllib2.urlopen(url)

    except urllib2.HTTPError, err:
      self.log.error("%s: %s", url, err)

    data = json.load(f)

    # Original setting for only publishing basicStats
    #self.publish("items.count", data["basicStats"]["itemCount"])

    statobjname = "basicStats"
    [self.publish("%s.%s" % (statobjname,basicStatsKey), data[statobjname][basicStatsKey]) for basicStatsKey in data[statobjname].keys()]

    statobjname = "nodes"

    for nodeelem in data[statobjname]:
      # We are only interested in the node stats for this node; for other nodes another diamond collector will be running
      if "thisNode" in nodeelem.keys():
        nodepath = "thisnode"

        [self.publish("%s.%s" % (statobjname,interestingStatsKey), nodeelem["interestingStats"][interestingStatsKey]) for interestingStatsKey in nodeelem["interestingStats"].keys()]
        
    statobjname = "quota"
    [self.publish("%s.%s" % (statobjname,quotaKey), data[statobjname][quotaKey]) for quotaKey in data[statobjname].keys()
]

    self.log.info("collected!")

