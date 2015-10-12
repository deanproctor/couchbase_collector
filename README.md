Couchbase Collector for Diamond
=====

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

#### Options

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>enabled</td><td>False</td><td>Enable collecting these metrics</td><td>bool</td></tr>
<tr><td>host</td><td>localhost</td><td>The hostname(:port) to get metrics from</td><td>str</td></tr>
<tr><td>user</td><td>Administrator</td><td>Admin username for authentication. Recommendation: use read-only admin</td><td>str</td></tr>
<tr><td>passwd</td><td>password</td><td>Admin password for authentication</td><td>str</td></tr>
<tr><td>ssl</td><td>False</td><td>True to enable SSL connections</td><td>bool</td></tr>
<tr><td>buckets</td><td>all</td><td>A list of buckets to get metrics from. The default is to query all buckets</td><td>list</td></tr>
<tr><td>stats</td><td>all</td><td>The list of stats to save.  The default is to save everything</td><td>list</td></tr>
<tr><td>ignore</td><td></td><td>The list of stats to exclude. Useful when 'stats' = 'all'</td><td>list</td></tr>
</table>

