# coding=utf-8

"""
Collect statistics from the Couchbase Buckets API.  
See: http://docs.couchbase.com/admin/admin/REST/rest-bucket-intro.html 

#### Dependencies

 * json
 * urllib2

#### Example Configuration

CouchbaseCollector.conf

```
    enabled = True
    host    = 192.168.56.101:8091
    buckets = default, sessions
    stats   = cmd_get, cmd_set, couch_docs_fragmentation, couch_views_fragmentation, curr_connections, curr_items, decr_hits, decr_misses, delete_hits, delete_misses, ep_bg_fetched, ep_dcp_2i_items_remaining, ep_dcp_other_backoff, ep_dcp_other_count, ep_dcp_other_items_remaining, ep_dcp_other_items_sent, ep_dcp_other_producer_count, ep_dcp_other_total_bytes, ep_dcp_replica_backoff, ep_dcp_replica_count, ep_dcp_replica_items_remaining, ep_dcp_replica_items_sent, ep_dcp_replica_total_bytes, ep_dcp_xdcr_backoff, ep_dcp_xdcr_count, ep_dcp_xdcr_items_remaining, ep_dcp_xdcr_items_sent, ep_dcp_xdcr_producer_count, ep_dcp_xdcr_total_bytes, ep_diskqueue_drain, ep_diskqueue_fill, ep_diskqueue_items, ep_flusher_todo, ep_kv_size, ep_mem_high_wat, ep_oom_errors, ep_queue_size, ep_resident_items_rate, ep_tmp_oom_errors, incr_hits, incr_misses, mem_used, vb_active_queue_age, vb_active_queue_drain, vb_active_queue_fill, vb_active_queue_size, vb_active_resident_items_ratio, vb_avg_total_queue_age, vb_pending_queue_age, vb_pending_queue_drain, vb_pending_queue_fill, vb_pending_queue_size, vb_replica_queue_age, vb_replica_queue_drain, vb_replica_queue_fill, vb_replica_queue_size, vb_replica_resident_items_ratio
    ignore = timestamp
```
"""

import diamond.collector
import urllib2
import base64

try:
  import json
except ImportError:
  import simplejson as json

class CouchbaseCollector(diamond.collector.Collector):

  def get_default_config_help(self):
    config_help = super(CouchbaseCollector, self).get_default_config_help()
    config_help.update({
      'host':    'The hostname(:port) to get metrics from',
      'user':    'Admin username for authentication (Recommendation: use read-only admin)',
      'passwd':  'Admin password for authentication',
      'ssl':     'True to enable SSL connections.  Default is False',
      'buckets': 'A list of buckets to get metrics from. Defaults to \'all\' which will query all buckets',
      'stats':   'The list of stats to save.  Defaults to \'all\' which will save everything',
      'ignore':  'The list of stats to exclude. Useful when \'stats\' = \'all\'' 
    })
    return config_help

  def get_default_config(self):
    config = super(CouchbaseCollector, self).get_default_config()
    config.update({
      'host':    'localhost',
      'user':    'Administrator',
      'passwd':  'password',
      'ssl':     False,
      'buckets': 'all',
      'stats':   'all',
      'ignore':  []
    })
    return config

  def _couchbase_api(self, bucket=None):
    host = self.config['host']
    if ':' not in host:
      host = host + ':8091'
    
    if self.config['ssl'] is True:
      protocol = 'https'
    else:
      protocol = 'http'
    
    url = protocol + '://' + host + '/pools/default/buckets/' 

    if bucket is not None:
      url = url + bucket + '/stats'

    auth_string = base64.encodestring('%s:%s' % (self.config['user'], self.config['passwd']))

    request = urllib2.Request(url);
    request.add_header("Authorization", "Basic %s" % auth_string)

    try:
      f = urllib2.urlopen(url)
      return json.load(f)
    except urllib2.HTTPError, err:
      self.log.error("CouchbaseCollector: %s, %s", url, err)
    
  def collect(self):
    buckets = self.config['buckets']

    if buckets == 'all':
      buckets = []
      [buckets.append(bucket['name']) for bucket in self._couchbase_api()] 

    if isinstance(buckets, basestring):
      buckets = [buckets]

    for bucket in buckets:
      data = self._couchbase_api(bucket)
      if not data:
        continue

      metrics = data['op']['samples']

      stats = self.config['stats']
      ignore = self.config['ignore']

      for metric in metrics:
        if (metric in stats or stats == 'all') and metric not in ignore:
          avg_value = sum(metrics[metric], 0.0) / len(metrics[metric])
          self.publish("%s.%s" % (bucket, metric), avg_value)

