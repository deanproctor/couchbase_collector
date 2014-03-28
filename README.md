Cloned repo from https://github.com/zooldk/couchbase_collector

It expands the previous repo by collecting all metrics under:

"nodes" : [ "interestingStats" ]
"basicStats"
"quota"

keys from the returned couchbase json object.

You need to place it under a directory called couchbase_collector under /usr/share/diamond/collectors or wherever your diamond collector code resides

You also need a configuration file CouchBaseCollector.conf under /etc/diamond/collector (or wherever you collector configuration files reside) with the following content:

enabled = True

That should be it.

Configuration parameters for couchbase (host, port, path, name, password) need to be placed inside the get_default_config method in the CouchBaseCollector class.


Once you restart diamond you should be able to see entries like (metrics are from the beer-sample example in couchbase):

mytestserver.beer-sample.basicStats.diskUsed: 25565808
mytestserver.beer-sample.basicStats.memUsed: 35407008
mytestserver.beer-sample.basicStats.diskFetches: 0.0
mytestserver.beer-sample.basicStats.quotaPercentUsed: 33.7667541504
mytestserver.beer-sample.basicStats.opsPerSec: 0.0
mytestserver.beer-sample.basicStats.dataUsed: 24288256
mytestserver.beer-sample.basicStats.itemCount: 7303
mytestserver.beer-sample.nodes.couch_views_data_size: 543142
mytestserver.beer-sample.nodes.couch_docs_actual_disk_size: 56489751
mytestserver.beer-sample.nodes.couch_views_actual_disk_size: 564012
mytestserver.beer-sample.nodes.ops: 0.0
mytestserver.beer-sample.nodes.vb_replica_curr_items: 0
mytestserver.beer-sample.nodes.cmd_get: 0.0
mytestserver.beer-sample.nodes.mem_used: 99496312
mytestserver.beer-sample.nodes.get_hits: 0.0
mytestserver.beer-sample.nodes.curr_items: 7889
mytestserver.beer-sample.nodes.ep_bg_fetched: 0.0
mytestserver.beer-sample.nodes.curr_items_tot: 7889
mytestserver.beer-sample.nodes.couch_docs_data_size: 55645339
mytestserver.beer-sample.quota.ram: 104857600
mytestserver.beer-sample.quota.rawRAM: 104857600

