import diamond.collector
import json
import simplejson as json
import urllib2
import base64

class CouchBaseCollector(diamond.collector.Collector):

  def get_default_config(self):
    config = super(CouchBaseCollector, self).get_default_config()
    config.update({
      'host':        'localhost',
      'port':        8091,
      'path':        'couchbase',
      'username': 'admin',
      'password': 'password'
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

    [self.publish(basicStatsKey, data["basicStats"][basicStatsKey]) for basicStatsKey in data["basicStats"].keys()]

    self.log.info("collected!")

