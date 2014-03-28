import diamond.collector
import json
#import simplejson as json
import urllib2
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

    thenode = "basicStats"
    [self.publish("%s.%s" % (thenode,basicStatsKey), data[thenode][basicStatsKey]) for basicStatsKey in data[thenode].keys()]

    thenode = "nodes"
    [self.publish("%s.%s" % (thenode,interestingStatsKey), data[thenode][0]["interestingStats"][interestingStatsKey]) for interestingStatsKey in data[thenode][0]["interestingStats"].keys()]                                      

    thenode = "quota"
    [self.publish("%s.%s" % (thenode,quotaKey), data[thenode][quotaKey]) for quotaKey in data[thenode].keys()
]

    self.log.info("collected!")

