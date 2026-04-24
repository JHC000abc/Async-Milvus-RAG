Release Notes
Find out what’s new in Milvus! This page summarizes new features, improvements, known issues, and bug fixes in each release. You can find the release notes for each released version after v2.6.0 in this section. We suggest that you regularly visit this page to learn about updates.
v2.6.13
Release date: March 23, 2026
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.13
2.6.10
2.6.11
2.6.16
2.6.1
Features
Gemini embedding model support (
#48223
)
Added Google Gemini as a built-in text embedding function. Users can now use Gemini embedding models directly in Milvus by configuring a Gemini API key, including the recently released
Gemini Embedding 2
.
For detailed usage, refer to
Google Gemini
.
Improvements
Unified KV path/key conventions across etcd, tikv, and catalog layers with consistent path joining (
#48133
)
Added query metrics for JSON-related filter expressions to improve observability of JSON field query performance (
#48147
)
Reduced transient memory allocations in BM25Stats deserialization by eliminating temporary slices (
#48178
)
Added TruncateCollection method to the Go SDK client for clearing all data in a collection without dropping it (
#48361
)
Bug fixes
Fixed an issue where search/query requests with strong consistency timed out during compaction due to tsafe advancement being blocked (
#47987
)
Fixed an issue where partial upsert with dynamic fields failed with
the length of valid_data of field($meta) is wrong
when the batch contained both existing and new rows (
#48085
)
Fixed TLS connection failures during internal proxy-to-proxy request forwarding (
#48226
)
Fixed query failures when using IN combined with != filter expressions that form tautologies (
#48261
)
Fixed high system load caused by mass concurrent client disconnections during HTTP request handling (
#48270
)
Fixed an issue where queries could become unavailable during replica scale-up/down due to non-deterministic node-to-replica assignment (
#48277
)
Fixed HTTP proxy crashes caused by concurrent write race condition in timeout middleware (
#48296
,
#48317
,
#48356
)
Fixed potential query node crash caused by assertion failure in delete record snapshot handling (
#48302
)
Fixed storage operation failures when using AK/SK authentication on Aliyun OSS (
#48311
)
Fixed degraded search performance caused by permanent parameter cache failure leading to goroutine contention on proxy hot paths (
#48313
,
#48326
)
Fixed QueryCoord deadlock during upgrades when hundreds of channels needed rebalancing by splitting the executor into separate channel and non-channel task pools (
#48351
)
Fixed an issue where search requests could timeout for 14+ minutes after WAL ownership changes due to unbounded message replay during scanner catchup (
#48391
)
v2.6.12
Release date: March 17, 2026
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.12
2.6.10
2.6.11
2.6.15
2.6.1
We are pleased to announce the release of Milvus v2.6.12! This release introduces replication topology inspection and configurable TLS minimum version for object storage. It also delivers significant memory optimizations in segment loading and compaction, along with numerous bug fixes addressing memory leaks, RBAC alias resolution, collection-level rate limiting, and streaming node stability.
Features
Added
GetReplicateConfiguration
API for viewing replication topology with redacted tokens (
#47543
)
Added configurable TLS minimum version (
minio.ssl.tlsMinVersion
) for object storage connections across all supported backends (
#48000
,
#48030
)
Supported configuring different replica numbers on secondary CDC cluster independently from the primary (
#47914
)
Allowed pchannel count increase in CDC ReplicateConfiguration to support heterogeneous cluster topologies (
#47917
)
Added automatic warmup for large tenant collections to reduce cold-start query latency (
#47631
)
Added user-specified warmup support for RESTful API (
#47825
)
Improvements
Added caching layer resource management for streaming node with automatic memory/disk accounting during segment operations (
#47165
)
Optimized query node segment load speed (
#47424
)
Optimized MixCoord CPU usage to reduce coordinator overhead (
#47619
)
Added phase-level timing logs and metrics for sort compaction (
#47674
)
Refactored cluster-level broadcast mechanism to decouple message package from channel registration lifecycle (
#47807
)
Added configurable skip list for replicate message types in CDC (
#47910
)
Included text index memory cost in segment loading memory estimation (
#47963
)
Added per-cluster TLS configuration support for CDC outbound mTLS connections (
#48023
)
Bypassed broadcaster for resource group DDL operations on non-primary clusters in streaming replication (
#48034
)
Bumped OpenTelemetry to v1.40.0 to address CWE-426 untrusted search path vulnerability (
#48059
)
Bug fixes
Fixed an issue where collection-level rate limits were not delivered to proxies when set via collection properties (
#46714
,
#48018
)
Fixed memory accumulation during segment loading by switching to streaming cell-based loading (
#47859
)
Fixed streaming node crash-loop during WAL replay for dropped collections (
#47887
)
Fixed memory accumulation in compaction by streaming row groups one at a time (
#47904
)
Fixed memory leak in broadcaster caused by uncanceled context (
#47912
)
Fixed an issue where CreateCollection could cause schema loss on crash (
#47972
)
Fixed crash when inserting non-nullable fields with default values (
#48016
)
Fixed deadlock when loading V1 segments with more than 16 system field binlog files (
#48037
)
Fixed partial update failure when dynamic field is enabled but upsert data contains only static fields (
#48044
)
Fixed RBAC permission checks to resolve collection aliases and added automatic grant cleanup on collection drop/rename (
#48052
,
#48151
)
Fixed BulkInsert failure by removing interactive coordination between import and L0 compaction (
#48114
)
Fixed Azure buffered output stream issue (
#48041
)
v2.6.11
Release date: February 12, 2026
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.11
2.6.9
2.6.9
2.6.13
2.6.1
We are pleased to announce the release of Milvus 2.6.11! This update continues to enhance query performance and system stability with improvements to filtering execution, segment loading, and Storage V2 I/O pipelining. It also refines geo indexing, reduces memory usage in default-value chunks, and improves developer and build tooling through dependency and test-suite cleanups. This release further fixes several correctness issues across control-channel handling, index building, nullable-expression semantics, and WAL recovery workflows. We recommend all users on the 2.6 branch upgrade to this version for improved reliability and performance.
Features
Added a truncate API to remove collection data more efficiently (
#47308
)
Improvements
Used
PreparedGeometry
to improve geo index refinement performance (
#47389
)
Switched the OpenSSL dependency to shared linking (
#47664
)
Differentiated load priorities by scenario to improve scheduling behavior (
#47594
)
Upgraded Go to 1.24.12 and updated
gpgv
to address CVEs (
#47562
)
Reduced memory usage by enabling multi-cell
DefaultValueChunk
layout (
#47166
)
load-diff based segment loading patches to improve load efficiency (
#47545
)
Removed redundant bitset count operations during filter execution to reduce CPU overhead (
#47546
)
Added semantic highlighting support for dynamic fields (
#47464
)
Reduced unnecessary
PinWrapper
copies in
searchPksWith
to improve query performance (
#47531
)
Normalized constant-folded boolean expressions to
AlwaysTrueExpr
/
AlwaysFalseExpr
during rewriting for simpler plans (
#47493
)
Added RESTful
search_by_pk
support (
#47318
)
Optimized “latest delete snapshot” handling to reduce overhead (
#47409
)
Added support for user-specified warmup settings (
#47343
)
Added
LoadWithStrategyAsync
to enable true I/O pipelining in Storage V2 (
#47427
)
Optimized MixCoord’s CPU and memory usage by avoiding redundant calculations in the balance checker (
#47190
)
Added sparse filtering support in search (
#47447
)
Reduced memory allocations and copies during data loading (
#47088
)
Bug fixes
Fixed an issue where collection metadata could contain an invalid database name (
#47721
)
Ensured exclusive control-channel messages acquire a global lock in the lock interceptor (
#47678
)
Fixed channel exclusive mode state loss and vchannel list handling issues (
#47702
)
Fixed index building to use the correct global offset for
null_offset
in
BuildIndexFromFieldData
(
#47708
)
Improved v2.5/v2.6 compatibility handling in
SyncTargetVersion
(QueryNode) (
#47693
)
Handled
broadcastToAll
messages on the control channel in recovery storage (
#47640
)
Added
warmupKey
to the
CheckParams
filter to make
CreateIndex
idempotent (
#47607
)
Corrected the default
mmap
value in code (
#47490
)
Populated
LevelZeroSegmentIDs
in
GetDataVChanPositions
(
#47597
)
Corrected null handling on
NullExpr
,
ExistsExpr
, and logical operators (
#47519
)
Removed
segment_loader
pre-reserve logic for warmup fields/indexes to avoid incorrect reservations (
#47463
)
Updated
log_*
macros to use
{}
placeholders to avoid treating error messages as format strings (
#47485
)
Fixed bloom filter memory leak when a worker node crashes (
#47451
)
Used actual data timestamps for imported segment positions (
#47370
)
Rebuilt WAL messages on each append retry to avoid panics (
#47480
)
Filled in the log and memory size fields in
TextIndexStats
metadata (
#47476
)
Reduced the empty timetick filtering interval to improve timetick handling (
#47471
)
v2.6.10
Release date: February 5, 2026
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.10
2.6.8
2.6.9
2.6.13
2.6.1
We are pleased to announce the release of Milvus 2.6.10! This update strengthens security controls around KMS key revocation and improves search and storage performance through automatic FP32-to-FP16/BF16 conversion, optimized segment loading, and updated auto-index configurations. This release also fixes a number of stability issues across compaction, query pagination, and recovery workflows. We recommend all users on the 2.6 branch upgrade to this version for improved reliability and performance.
Improvements
Added support to stop WAL consumption when a KMS key is revoked (
#47018
)
Updated the default auto-index configuration for vector fields (
#47388
)
Disabled storage-version upgrade compaction by default (
#47383
)
Added automatic FP32-to-FP16/BF16 conversion in search (
#47241
)
Limited segment load concurrency by submitting loads to the load pool (
#47335
)
Added the
map_populate
flag for
mmap
to reduce page faults during access (
#47317
)
Persisted BM25 stats to disk during segment loading to reduce recomputation (
#47232
)
Added loading timeout and cancellation support for better control of long-running loads (
#47223
)
Allowed
alter_collection_field()
to update the field description (
#47058
)
Added a target manager to
ReplicaObserver
initialization (
#47093
)
Updated the Knowhere version for vector search improvements (
#47109
)
Added BM25
search_by_pk
support (
#47012
)
Extracted assign policy from the balancer and added
StoppingBalancer
(
#47138
)
Prevented import jobs/tasks from rolling back state unexpectedly (
#47102
)
Improved slow logs by recording average cost per NQ (
#47086
)
Bug fixes
Fixed incorrect group results during pagination of grouped queries (
#47248
)
Added boundary validation for threadpool resize operations (
#47367
)
Improved error message handling when the error type is missing (
#47369
)
Prevented coredumps and improved diagnostics for
PhyReScoresNode
(
#47341
)
Reverted a compaction change related to “fast finish” when L0 compaction hits zero (L1/L2) (
#47336
)
Prevented server crashes on division/modulo by zero in filter expressions (
#47306
)
[Go SDK] Aligned
timestamptz
field type and data format with the server (
#47328
)
Added authentication to the metrics endpoint when authorization is enabled (
#47278
)
Updated
milvus_proxy_req_count
metrics for RESTful APIs (
#47239
)
Submitted
TriggerTypeStorageVersionUpgrade
compaction tasks correctly (
#47234
)
Allowed empty compaction results (
#47153
)
Fixed Azure precheck to use a fixed bucket not owned by Milvus (
#47168
)
Ignored L0 compaction during
PreallocSegmentIDs
checks (
#47189
)
Fixed compaction fast-finish behavior when L0 compaction hits zero (L1/L2) (
#47187
)
Removed unnecessary batching to reduce OOM risk (
#47175
)
Fixed deserialization handling for empty vector arrays (
#47127
)
Fixed runtime config updates not triggering watchers (
#47161
)
Unified primary-key handling logic between
deletePreExecute
and
packDeleteMessage
(
#47147
)
Used user-provided target size in compaction-related logic (
#47115
)
v2.6.9
Release date: January 16, 2026
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.9
2.6.6
2.6.9
2.6.13
2.6.1
We are pleased to announce the release of Milvus 2.6.9! This update introduces highlight scores for search results, enhances segment management with support for reopening segments when data or schema changes occur, and improves storage version handling. Key improvements include better logging performance, enhanced security controls for expression endpoints, and optimizations for text analyzers and index building. This release also resolves critical issues including memory estimation accuracy, geometry data conversions, and various stability fixes. We recommend all users on the 2.6 branch upgrade to this version for improved system reliability and performance.
Features
Supported searching by primary keys (
#46528
)
Improvements
Added a storage version label metric for better observability (
#47014
)
QueryCoord now supports segment reopen when manifest path changes (
#46921
)
Added support for reopening segments when data or schema changes occur (
#46412
)
Improved slow log performance and efficiency (
#47086
)
Added storage version upgrade compaction policy to facilitate version migrations (
#47011
)
Eliminated extra memory copy operations for C++ logging to improve performance (
#46992
)
Added security controls for the /expr endpoint to prevent unauthorized access (
#46978
)
Streaming service now remains enabled until the required streaming node count is reached (
#46982
)
Removed redundant etcd put operations when updating segment information (
#46794
)
Improved row count validation and reduced misleading warning logs for sort compaction (
#46824
)
Cleaned up and organized build index log messages (
#46769
)
Limited the number of concurrent vector index builds per worker to prevent resource exhaustion (
#46877
)
Optimized jieba and lindera analyzer cloning operations for better performance (
#46757
)
Added glog sink to transfer CGO logs into zap logger for unified logging (
#46741
)
Enforced storage V2 format usage and deprecated V1 writes (
#46889
)
Implemented batch processing for ngram operations to improve efficiency (
#46703
)
Added automatic retry mechanism for binlog write operations to improve reliability (
#46854
)
Filtered empty timetick messages from the consuming side to reduce unnecessary processing (
#46730
)
Improved search by primary key with duplicate checking and automatic anns_field inference (
#46745
)
Added dimension parameter support for siliconflow and cohere embedding providers (
#47081
)
Bug fixes
Fixed double counting of index memory in segment loading estimation (
#47046
)
Fixed compilation issues on macOS 14 (
#47048
)
Used revision as streaming service discovery global version for better consistency (
#47023
)
Ensured all futures complete on exception to prevent use-after-free crashes (
#46960
)
Fixed shard interceptor incorrectly skipping
FlushAllMsg
operations (
#47004
)
Added valid range validation for collection TTL to prevent invalid configurations (
#47010
)
Fixed
GetCredentialInfo
not caching RPC responses (
#46945
)
Fixed issue where
AlterFunction
could not be invoked when multiple functions become invalid (
#46986
)
Fixed inverted index null offset file not being compacted (
#46950
)
Fixed crash when using is_null_expr on indexed JSON fields (
#46894
)
Added check for allow_insert_auto_id flag in RESTful v2 insert API (
#46931
)
Added field existence check in column groups before reading from loon manifest (
#46924
)
Fixed bug where the highlight parameter was not working correctly (
#46876
)
Quota center now ignores delegator when it is in recovering state (
#46858
)
Aligned WKT/WKB conversion options to ensure consistent behavior across operations (
#46874
)
Fixed voyageai model int8 bug (
#46821
)
Fixed missing handling of
FlushAllMsg
in recovery storage operations (
#46803
)
Fixed missing shardclientmgr field in querytask to prevent panic (
#46838
)
Used leaderid for leaderaction stale check in scheduler to improve accuracy (
#46788
)
Restored tenant/namespace support for Pulsar that was lost in 2.6 (
#46759
)
Added load config watcher to prevent load config modifications from being lost (
#46786
)
Fixed function edit interface bug (
#46782
)
Added collection TTL property validation to prevent compaction from getting stuck (
#46736
)
v2.6.8
Release date: January 4, 2026
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.8
2.6.6
2.6.9
2.6.11
2.6.1
We are excited to announce the release of Milvus 2.6.8! This version introduces search result highlighting, significantly enhancing the retrieval experience. Under the hood, we have optimized query processing, resource scheduling, and caching mechanisms to deliver superior performance and stability. Additionally, this release addresses critical bugs related to data security, storage handling, and concurrency. We highly recommend all users upgrade to this version for a more efficient and reliable production environment.
Features
Supported search with highlighter. For details, refer to
Text Highlighter
.  (
#46052
)
Improvements
Moved query optimization logic to the Proxy to improve performance (
#46549
)
Optimized
LIKE
operator performance using STL sort (
#46535
)
Enabled concurrent execution of text index tasks for multiple fields (
#46306
)
Supported pausing GC at the collection level (
#46201
)
Implemented a penalty policy for QueryNodes to handle resource exhaustion (
#46086
)
Optimized data caching by mapping multiple row groups to a single cache cell (
#46542
)
Reduced CPU usage in QuotaCenter (
#46615
)
Improved
TIMESTAMPTZ
data comparison performance (
#46655
)
Supported nullable dynamic fields with an empty JSON object as the default value (
#46445
)
Prevented unnecessary segment sealing when only altering collection properties (
#46489
)
Supported DML and DQL forwarding in Proxy for RESTful v2 (
#46021
,
#46037
)
Added retry mechanism for object storage reads on rate limit errors (
#46464
)
Enhanced logging for Proxy and RootCoord meta tables (
#46701
)
Added validation for embedding models and schema field types (
#46422
)
Introduced a tolerance duration to delay collection drop operations (
#46252
)
Improved index task scheduling by estimating slots based on field size and type (
#46276
,
#45851
)
Added fallback mechanism for write paths when accessing object storage without condition write support (
#46022
)
Optimized IDF oracle synchronization logic (
#46079
)
Changed RootCoord default port to a non-ephemeral port (
#46268
)
Added metrics to monitor Jemalloc cached memory (
#45973
)
Improved disk quota metric accuracy when cluster quota changes (
#46304
)
Improved trace observability for scalar expressions (
#45823
)
Rejected duplicate primary keys in upsert batch requests (
#46035
)
Bug fixes
Fixed RBAC ETCD prefix matching to prevent potential data leakage (
#46708
)
Fixed incorrect root path handling for local storage mode (
#46693
)
Fixed handling of mixed
int64
/
float
types in JSON fields (
#46682
)
Fixed text log loading failures during cluster upgrade (
#46698
)
Prevented deletion of other fields during raw data cleanup (
#46689
)
Fixed failure when using highlighting with multiple analyzers (
#46664
)
Ensured logs are flushed when the OS exits (
#46609
)
Fixed ETCD RPC size limit exceeded error when dropping collections (
#46645
)
Fixed replication lag issues when the server is idle (
#46612
)
Fixed validation for invalid
TIMESTAMPTZ
default values (
#46556
)
Fixed restoration of compaction tasks to ensure proper cleanup (
#46578
)
Unified read-only node handling to avoid stuck balance channel tasks (
#46513
)
Prevented field data drops for multi-field column groups (
#46425
)
Removed stale proxy clients when re-watching ETCD (
#46490
)
Fixed chunk iterator merge order (
#46462
)
Prevented creation of Kafka consumer groups by disabling auto-commit (
#46509
)
Prohibited hot-reloading of tiered storage parameters (
#46438
)
Enabled search iterator for binary vectors (
#46334
)
Fixed race condition in storage initialization (
#46338
)
Fixed highlight queries not working for non-BM25 searches (
#46295
)
Fixed stack overflow during JSON garbage collection (
#46318
)
Ensured retries when writing binlogs (
#46310
)
Fixed index usage check for JSON fields (
#46281
)
Prevented target update blocking when replicas lack nodes during scaling (
#46291
)
Restricted
char_group
tokenizer to support only one-byte delimiters (
#46196
)
Skipped JSON path index usage if the query path includes numbers (
#46247
)
Fixed path concatenation errors in MinIO when root path is “.” (
#46221
)
Fixed false-positive health checks by correcting replicate lag metric calculation (
#46122
)
Fixed RESTful v2 parsing and schema defaults with
TIMESTAMPTZ
(
#46239
)
Fixed panic when searching empty results with output geometry fields (
#46231
)
Added field data alignment validation to prevent panics during partial updates (
#46180
)
Fixed database loss issue in RESTful v2 (
#46172
)
Fixed incorrect context usage in gRPC client sessions (
#46184
)
Fixed incorrect authorization forwarding in RESTful v2 during upgrades (
#46140
)
Fixed incorrect struct reduction logic (
#46151
)
Fixed error return from highlighter when search results are empty (
#46111
)
Corrected logic for loading raw data for fields (
#46155
)
Fixed cursor movement issue after skipping chunks in index (
#46055
)
Corrected loop logic for
TIMESTAMPTZ
scalar index output (
#46110
)
Fixed setting default values for geometry fields via RESTful API (
#46064
)
Implemented fast fail if any component is not ready on startup (
#46070
)
v2.6.7
Release date: December 4, 2025
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.7
2.6.4
2.6.5
2.6.10
2.6.1
Milvus 2.6.7 is a critical stabilization update for the 2.6.x series. This release focuses on hardening the system against distributed failures and optimizing resource utilization under high load. With significant improvements in I/O handling, memory management, and Kubernetes integration, we strongly recommend all production users upgrade to this version to ensure greater reliability and smoother operation at scale.
Features
Added
/livez
endpoint to support Kubernetes native liveness probes, improving container orchestration stability (
#45481
).
Added support for
GroupBy
operations on
TIMESTAMPTZ
fields, enhancing time-series analytics capabilities (
#45763
)
Supported
mmap
for JSON shredding’s shared key indices to reduce RAM footprint (
#45861
)
Improvements
Supported DML request forwarding in the Proxy to improve write availability and routing resilience (
#45922
).
Upgrade etcd to v3.5.23 to address consensus stability and performance regressions (
#45953
).
Added robust error handling for Etcd server crashes to prevent cascading component failures (
#45633
).
Reduced Etcd load by removing expensive watchers for simple session liveness checks (
#45974
).
Enhanced the WAL retention strategy to better balance disk usage with data recovery safety (
#45784
).
Supported asynchronous write syncing for logs to prevent disk I/O blocking from affecting the main execution path (
#45806
).
Enforced Buffered I/O usage for high-priority load tasks to optimize OS page cache utilization and throughput (
#45958
).
Optimized
mmap
strategy to map group chunks in a single system call, reducing kernel overhead during segment loading (
#45893
).
Improved the accuracy of memory estimation for JSON shredding to prevent OOM kills or under-utilization (
#45876
).
Refined segment load estimation to account for both eviction and warmup states (
#45891
).
Added granular cancellation checks in query operators to allow faster termination of aborted or timed-out queries (
#45894
).
Removed redundant resource type checks in file resource configuration (
#45727
).
Bug fixes
Interleaved Go and C++ logs into a unified stream to provide a correct chronological view for debugging (
#46005
).
Resolved a race condition where
LastConfirmedMessageID
could be incorrect under high concurrency writes (
#45874
).
Fixed a calculation error in aggregating
allsearchcount
from multiple search results (
#45904
).
Fixed Term expressions to correctly handle string containment logic within JSON arrays (
#45956
).
Replaced
json.doc()
with
json.dom_doc()
in
JSONContainsExpr
to fix parsing behaviors and improve performance (
#45786
).
Fixed a panic in Standby MixCoord components during the shutdown sequence (
#45898
).
Fixed the leader checker to ensure segment distribution is correctly synchronized to Read-Only nodes (
#45991
).
Ensured
HandleNodeUp
is triggered during node re-watching to maintain correct load balancing topology (
#45963
).
Implemented fallback to remote WAL storage if local WAL storage becomes unavailable (
#45754
).
Added
EmptySessionWatcher
to prevent panics when running in IndexNode binding mode (
#45912
).
Ensured memory state consistency when recovering broadcast tasks from protocol buffers (
#45788
).
Addressed thread-safety issues in SegCore collection schema updates (
#45618
).
Enforced Access Control (RBAC) checks for
ListImport
and
GetImportProgress
APIs (
#45862
).
Fixed a bug where BulkImport would fail if the input contained an empty struct list (
#45692
).
v2.6.6
Release date: November 21, 2025
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.6
2.6.3
2.6.4
2.6.8
2.6.1
We are excited to announce the release of Milvus 2.6.6, featuring a range of powerful new capabilities, performance enhancements, and essential bug fixes. This update introduces important features such as Geospatial and Timestampz data type, Boost ranker for rescoring, etc. This release also has many crucial scalar filtering performance improvements. Several critical bugs have also been addressed to ensure greater stability and reliability. With this release, Milvus continues to provide a more robust and efficient experience for all users. Below are the key highlights of this release.
Geospatial Data Type: Milvus introduces support for the
Geometry
data type, representing OGC-compliant geometric objects such as
POINT
,
LINESTRING
, and
POLYGON
. This type supports multiple spatial relationship operators (st_contains, st_intersects, st_within, st_dwithin, …) and provides an
RTREE
spatial index to accelerate spatial filtering and query execution. This enables efficient storage and querying of geospatial shapes for LBS, mapping, and other spatial workloads.
Timestamptz Data Type: Milvus introduces the TIMESTAMPTZ data type, providing timezone awareness for all temporal data. This feature enables consistent data management across global deployments by allowing users to define a default time context using the timezone property on Databases and Collections. Crucially, the field fully supports expression-based filtering for time range queries, and retrieval operations (query and search) support a timezone parameter for instant, on-the-fly conversion of timestamps into the required local format upon output.
Boost Ranker: Instead of relying solely on semantic similarity calculated based on vector distances, Boost Ranker allows Milvus to use the optional filtering condition within the function to find matches among search result candidates and boosts the scores of those matches by applying the specified weight, helping promote or demote the rankings of the matched entities in the final result.
STL_SORT index now supports VARCHAR and TIMESTAMPTZ datatype.
You may now enable dynamic field of an existing collection by altering it.
Fixed cve-2025-63811.
Features
Added new config and enabled dynamic update configs (
#45363
)
Improvements
Fixed cve-2025-63811 (
#45658
)
Removed large segment id arrays from querynode logs (
#45720
)
Updated multiple places where the expr copied the input values in every loop (
#45712
)
Optimized term expr performance (
#45671
)
Prefetched vector chunks for sealed non-indexed segments (
#45666
)
Expr: only prefetched chunks once (
#45555
)
Added nullable support for geometry and timestamptz types (
#45522
)
Increased session ttl from 10s to 30s (
#45517
)
Added more metrics for ddl framework (
#45559
)
Updated maxconnections config version (
#45547
)
Skipped check source id (
#45519
)
Supported max_connection config for remote storage (
#45364
)
Prevented panic by adding null pointer check when clearing insertrecord pk2offset (
#45442
)
Performed some optimization of scalar field fetching in tiered storage scenarios (
#45361
)
Fixed typo of analyzer params (
#45434
)
Overrode index_type while creating segment index (
#45417
)
Added rbac support for updatereplicateconfiguration (
#45236
)
Bumped go version to 1.24.9 (
#45369
)
Disabled jsonshredding for default config (
#45349
)
Unified the aligned buffer for both buffered and direct i/o (
#45325
)
Renamed jsonstats related user config params (
#45252
)
Made knowhere thread pool config refreshable (
#45191
)
Cherry-picked patch of new ddl framework and cdc 3 (
#45280
)
Set schema version when creating new collection (
#45269
)
Supported jsonl/ndjson files for bulkinsert (
#44717
)
Waited for replicate stream client to finish (
#45260
)
Made geometrycache an optional configuration (
#45196
)
Cherry-picked patch of new ddl framework and cdc 2 (
#45241
)
Did not start cdc by default (
#45217
)
Cherry-picked patch of new ddl framework and cdc (
#45025
)
Removed max vector field number limit (
#45156
)
Showed create time for import job (
#45059
)
Optimized scalarindexsort bitmap initialization for range queries (
#45087
)
Enabled stl_sort to support varchar (
#45050
)
Extracted shard client logic into dedicated package (
#45031
)
Refactored privilege management by extracting privilege cache into separate package (
#45002
)
Supported json default values in fillfielddata (
#45470
)
Updated enabledynamicfield and schemaversion during collection modification (
#45616
)
Bug fixes
Fixed partial update panic with timestamptz (
#45741
)
Used 2.6.6 for milvus ddl upgrading (
#45739
)
Used latest timetick to expire cache (
#45699
)
Made streamingnode exit when it failed initializing (
#45732
)
Protected tbb concurrent_map emplace to avoid race condition deadlock (
#45682
)
Prevented panic when streaming coord shutdown but query coord still worked (
#45696
)
Set task init when worker didn’t have task (
#45676
)
Prevented deadlock in runcomponent when prepare failed (
#45647
)
Prevented panic when double closing channel of ack broadcast (
#45662
)
Corrected default value backfill during addfield (
#45644
)
Compacted the assignment history of channel to decrease the size of assignment recovery info (
#45607
)
Handled default values correctly during compaction for added fields (
#45619
)
Removed validatefieldname in dropindex (
#45462
)
Ignored compaction task when from segment was not healthy (
#45535
)
Set schema properties before broadcasting alter collection (
#45529
)
Stored database event if the key was invalid (
#45530
)
Fixed bulkimport bug for struct field (
#45536
)
Failed to get raw data for hybrid index (
#45408
)
Retained collection early to prevent it from being released before query completion (
#45415
)
Used the right resource key lock for ddl and used new ddl in transfer replica (
#45509
)
Fixed index compatibility after upgrade (
#45374
)
Fixed channel not available error and released collection blocking (
#45429
)
Removed collection meta when dropping partition (
#45497
)
Fixed target segment marked dropped for save stats result twice (
#45479
)
Wrongly updated timetick of collection info (
#45471
)
Added tzdata dependency to enable iana time zone id recognition (
#45495
)
Corrected field data offset calculation in rerank functions for bulk search (
#45482
)
Fixed filter geometry for growing with mmap (
#45465
)
Nextfieldid did not consider struct (
#45438
)
Group value was nil (
#45419
)
Provided accurate size estimation for sliced arrow arrays in compaction (
#45352
)
Fixed data race in replicate stream client (
#45347
)
Skipped building text index for newly added columns (
#45317
)
Accidentally ignored sealed segments in l0 compaction (
#45341
)
Moved finishload before text index creation to ensure raw data availability (
#45335
)
Did not use json_shredding for json path is null (
#45311
)
Cherry-picked fixes related to timestamptz (
#45321
)
Fixed load segment failure due to get disk usage error (
#45300
)
Supported json default value in compaction (
#45331
)
Computed the correct batch size for the geometry index of the growing segment (
#45261
)
Applied ddl framework bug patch (
#45292
)
Fixed alter collection failure with mmap setting for struct (
#45240
)
Initialized timestamp range in composite binlog writer (
#45283
)
Skipped creating tmp dir for growing r-tree index (
#45257
)
Avoided potential race conditions when updating the executor (
#45232
)
Allowed "[" and "]" in index name (
#45194
)
Fixed bug for shredding json when empty but not null json (
#45214
)
Ensured append operation could only be canceled by the wal itself but not the rpc (
#45079
)
Resolved wp gcp cloud storage access issue with ak/sk (
#45144
)
Fixed import null geometry data (
#45162
)
Added null check for packed_writer_ in jsonstatsparquetwriter::close() (
#45176
)
Failed to mmap emb_list_meta in embedding list (
#45126
)
Updated querynode numentities metrics when collection had no segments (
#45160
)
Prevented retry when importing invalid utf-8 strings (
#45068
)
Handled empty fieldsdata in reduce/rerank for requery scenario (
#45137
)
Fixed panic when gracefully stopping cdc (
#45095
)
Fixed auth token contamination, oss/cos support, redundant sync err logs (
#45106
)
Handled all-null data in stringindexsort to prevent load timeout (
#45104
)
Disabled building old version jsonstats from request (
#45102
)
Fixed bug for importing geometry data (
#45090
)
Fixed parquet import bug in struct (
#45071
)
Added getmetrics back to indexnodeserver to ensure compatibility (
#45074
)
Fixed alter collection failure for struct sub-fields (
#45042
)
Fixed collection level mmap not taking effect for struct (
#44997
)
Prevented data race in querycoord collection notifier update (
#45051
)
Handled json field default values in storage layer (
#45009
)
Double-checked to avoid iter being erased by other thread (
#45015
)
Fixed bug for gis function to filter geometry (
#44967
)
v2.6.5
Release date: November 11, 2025
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.5
2.6.3
2.6.4
2.6.7
2.6.1
We are excited to announce the release of Milvus 2.6.5, which addresses a
critical security vulnerability
CVE-2025-64513
and upgraded to Go 1.24.9. We strongly encourage
all Milvus 2.6.x users to upgrade to 2.6.5
as soon as possible. This update also includes several other improvements and bug fixes, and provides the users a more robust and efficient experience.
Improvements
Updated builder image tag upgrading go1.24.9 (
#45398
)
Skipped check source id (
#45379
)
Bug fixes
Group value is nil (
#45421
)
Initialized timestamp range in composite binlog writer  (
#45402
)
Handled empty fieldsdata in reduce/rerank for requery scenario  (
#45389
)
Added null check for packed_writer_ in jsonstatsparquetwrite… (
#45376
)
Skipped building text index for newly added columns (
#45358
)
Accidentally ignored sealed segments in l0 compaction (
#45351
)
Moved finishload before text index creation to ensure raw data availability (
#45336
)
Supported json default value in compaction (
#45332
)
Updated milvus-storage to fix duplicate aws sdk initialization  (
#45075
)
v2.6.4
Release date: October 21, 2025
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.4
2.6.3
2.6.1
2.6.6
2.6.1
We are excited to announce the release of Milvus 2.6.4, featuring a range of powerful new capabilities, performance enhancements, and essential bug fixes. This update introduces important features such as Struct in ARRAY for advanced data modeling. Additionally, we have enabled JSON Shredding by default, further improving query performance and efficiency. Several critical bugs have also been addressed to ensure greater stability and reliability. With this release, Milvus continues to provide a more robust and efficient experience for all users. Below are the key highlights of this release.
Features
Struct in ARRAY:  Milvus introduced the new data type, Struct, allowing users to organize and manage multiple related fields within a single entity. Currently, Struct can only be used as an element under DataType.ARRAY, enabling features like Array of Vector, where each row contains multiple vectors, opening up new possibilities for complex data modeling and search. (
#42148
)
Supported Qwen GTE-rerank-v2 model in DashScope (
#44660
)
Supported AISAQ index - an all in storage index (
#1282
)
Improvements
Upgraded Go version to 1.24.6
with image builder (
#44763
)
Enabled default JSON Shredding (
#44811
)
Added disk quota for loaded binlog size to prevent query node load failures (
#44932
)
Enabled mmap support for struct array in MemVectorIndex (
#44832
)
Added caching layer management for TextMatchIndex (
#44768
)
Optimized bitmap reverse lookup performance  (
#44838
)
Updated Knowhere version (
#44707
#44765
)
Removed logical usage checks during segment loading (
#44770
)
Added access log field for template value length information (
#44783
)
Allowed overwriting current index type during index build (
#44754
)
Added load parameters for vector index (
#44749
)
Unified compaction executor task state management (
#44722
)
Added refined logs for task scheduler in QueryCoord (
#44725
)
Ensured accesslog.$consistency_level represents actual value used  (
#44711
)
Removed redundant channel manager from datacoord (
#44679
)
Bug fixes
Removed GCC from build Dockerfile to fix CVE (
#44882
)
Ensured deterministic search result ordering when scores are equal (
#44884
)
Reranked before requery if reranker didn’t use field data (
#44943
)
Ensured promise fulfillment when CreateArrowFileSystem throws an exception (
#44976
)
Fixed missing disk encryption config (
#44839
)
Fixed deactivate balance checker causing balance stop issue (
#44836
)
Fixed issue where “not equal” doesn’t include “none”  (
#44960
)
Supported JSON default value in CreateArrowScalarFromDefaultValue (
#44952
)
Used short debug string to avoid newlines in debug logs (
#44929
)
Fixed exists expression for JSON flat index (
#44951
)
Unified JSON exists path semantics (
#44926
)
Fixed panic caused by empty internal insert message (
#44906
)
Updated AI/SAQ parameters (
#44862
)
Removed limit on deduplication when autoindex is disabled (
#44824
)
Avoided concurrent reset/add operations on DataCoord metrics (
#44815
)
Fixed bug in JSON_contains(path, int) (
#44818
)
Avoided eviction in caching layer during JSON handling (
#44813
)
Fixed wrong results from the exp filter when skipped (
#44779
)
Checked if query node is SQN with label and streaming node list (
#44793
)
Fixed BM25 with boost returning unordered results (
#44759
)
Fixed bulk import with auto ID (
#44694
)
Passed file system via FileManagerContext when loading index (
#44734
)
Used “eventually” and fixed task ID appearing in both executing and completed states (
#44715
)
Removed incorrect start time tick to avoid filtering DMLs with timeticks less than it (
#44692
)
Made AWS credential provider a singleton (
#44705
)
Disabled shredding for JSON path containing digits (
#44808
)
Fixed valid unit test for TestUnaryRangeJsonNullable (
#44990
)
Fixed unit tests and removed file system fallback logic (
#44686
)
v2.6.3
Release date: October 11, 2025
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.3
2.6.2
2.6.1
2.6.5
2.6.1
We are pleased to announce the release of Milvus 2.6.3, which introduces a variety of exciting new features, improvements, and critical bug fixes. This version enhances system performance, expands functionality, and fixes key issues, providing a more stable experience for all users. Below are the highlights of this release:
New Features
Primary Key with AutoID Enabled: Users can now write the primary key field when
autoid
is enabled. (
#44424
#44530
)
Manual Compaction for L0 Segments: Added support for manually compacting L0 segments. (
#44440
)
Cluster ID Encoding in AutoID: Auto-generated IDs will now include the cluster ID. (
#44471
)
gRPC Tokenizer Support: Integration of gRPC tokenizer for enhanced query flexibility. (
#41994
)
Improvements
Refined the balance checker by implementing a priority queue, improving task distribution. (
#43992
)
Preloaded BM25 stats for sealed segments and optimized serialization. (
#44279
)
Nullable fields can now be used as input for BM25 functions. (
#44586
)
Added support for Azure Blob Storage in Woodpecker. (
#44592
)
Purged small files right after Woodpecker segment compaction. (
#44473
)
Enabled random score functionality for boosting queries. (
#44214
)
New configuration options for the
int8
vector type in autoindexing. (
#44554
)
Added parameter items to control hybrid search requery policy. (
#44466
)
Added support for controlling the insertion of function output fields. (
#44162
)
The decay function now supports configurable score merging for better performance. (
#44066
)
Improved the performance of binary search on strings. (
#44469
)
Introduced support for sparse filters in queries.  (
#44347
)
Various updates to enhance tiered index functionality. (
#44433
)
Added storage resource usage tracking for scalar and vector searches. (
#44414
#44308
)
Add storage usage for delete/upsert/restful (
#44512
)
Enabled granular flush targets for
flushall
operations. (
#44234
)
Datanodes will now use a non-singleton file system for better resource management. (
#44418
)
Added configuration options for batch processing in metadata.  (
#44645
)
Error messages now include the database name for better clarity. (
#44618
)
Moved tracer test to the
milvus-common
repository for better modularization. (
#44605
)
Moved C API unit test files aside to
src
directory for better organization. (
#44458
)
Go SDK now allows users to insert primary key data if
autoid
is enabled. (
#44561
)
Bug fixes
Resolved CVE-2020-25576 and WS-2023-0223 vulnerabilities. (
#44163
)
Fixed an issue where logical resources were used for metrics in the quota center on streaming nodes. (
#44613
)
Set
mixcoord
in
activatefunc
when enabling standby. (
#44621
)
Removed redundant initialization of storage V2 components.
#44597
)
Fixed compaction task blocking due to executor loop exit. (
#44543
)
Refunded loaded resource usage in the
insert/deleterecord
destructor. (
#44555
)
Fixed an issue where the replicator could not stop and enhanced the replicate config validator. (
#44531
)
Set
mmap_file_raii
_ to
nullptr
when mmap is disabled. (
#44516
)
Made
diskfilemanager
use the file system from the context. (
#44535
)
Forced virtual host for OSS and COS in storage V2. (
#44484
)
Set
report_value
default value when
extrainfo
is not
nil
for compatibility. (
#44529
)
Cleaned up collection metrics after dropping collections in rootcoord. (
#44511
)
Fixed segment loading failure due to duplicate field
mmap.enable
properties. (
#44465
)
Fixed load config parsing errors for dynamic replicas. (
#44430
)
Handled row-to-column input for dynamic columns in Go SDK. (
#44626
)
v2.6.2
Release date: September 19, 2025
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.2
2.6.2
2.6.0
2.6.4
2.6.1
We’re excited to announce the release of Milvus 2.6.2! This update introduces powerful new features, significant performance enhancements, and critical fixes that make the system more stable and production-ready. Highlights include partial field updates with upsert, JSON Shredding to accelerate dynamic field filtering, NGram indexing for faster LIKE queries, and more flexible schema evolution on existing collections. Built on community feedback, this release delivers a stronger foundation for real-world deployments, and we encourage all users to upgrade to take advantage of these improvements.
Features
Added support for JSON Shredding to accelerate dynamic field filtering. For details, refer to
JSON Shredding
.
Added support for NGRAM Index to accelerate like operation. For details, refer to
NGRAM
.
Added support for partial field updates with upsert API. For details, refer to
Upsert Entities
.
Added support for Boost Function. For details, refer to
Boost Ranker
.
Added support for group by JSON fields and dynamic fields (
#43203
)
Added support for enabling dynamic schema on existing collections (
#44151
)
Added support for dropping indexes without releasing collections (
#42941
)
Improvements
[StorageV2] Changed log file size to compressed size (
#44402
)
[StorageV2] Added child fields in load info (
#44384
)
[StorageV2] Added support for including partition and clustering keys in system group (
#44372
)
Removed timeout for compaction tasks (
#44277
)
[StorageV2] Enabled build with Azure (
#44177
)
[StorageV2] Utilized group info for estimating logic usage (
#44356
)
[StorageV2] Utilized group split info to estimate usage (
#44338
)
[StorageV2] Saved column group results in compaction (
#44327
)
[StorageV2] Added configurations for size-based split policy (
#44301
)
[StorageV2] Added support for schema-based and size-based split policy (
#44282
)
[StorageV2] Added configurable split policy (
#44258
)
[CachingLayer] Added more metrics and configurations (
#44276
)
Added support for waiting for all indices to be ready before loading segments (
#44313
)
Added internal core latency metric for rescore node (
#44010
)
Optimized access log format when printing KV params (
#43742
)
Added configuration to modify dump snapshot batch size (
#44215
)
Reduced compaction task cleanup interval (
#44207
)
Enhanced merge sort to support multiple fields (
#44191
)(
#43994
)
Added load resource estimation for tiered index (
#44171
)
Added autoindex config for deduplication case (
#44186
)
Added configuration to allow custom characters in names  (
#44063
)
Added support for cchannel for streaming service (
#44143
)
Added mutex and range check to guard concurrent deletions (
#44128
)
Bug fixes
Aligned the behavior of exists expressions between brute force and index (
#44030
)
Fixed error on renaming to a dropped collection (
#44436
)
[StorageV2] Checked child fields length (
#44405
)
[StorageV2] Turned on Azure by default (
#44377
)
Corrected upload path of L0 compactions under pooling datanodes (
#44374
)
Disallowed renaming if database encryption is enabled (
#44225
)
Disallowed deletion of dynamicfield.enable property (
#44335
)
Marked tasks as failed when pre-allocated ID is invalid (
#44350
)
Skipped MVCC checks on PK compare expressions (
#44353
)
Fixed json_contains bug for stats (
#44325
)
Added initialization filesystem check for query node and streaming node (
#44360
)
Fixed empty compaction target when segment was garbage collected (
#44270
)
Fixed race condition when initializing timestamp index (
#44317
)
Checked if arraydata is nil to prevent panic (
#44332
)
Fixed build JSON stats bug for nested objects (
#44303
)
Avoided mmap rewrite by multiple JSON fields (
#44299
)
Unified valid data formats (
#44296
)
Hid credentials of embedding/reranking providers in web UI (
#44275
)
Corrected statslog path under pooling datanodes (
#44288
)
Corrected path of IDF oracle (
#44266
)
Used recovery snapshot checkpoint if no vchannel is recovering (
#44246
)
Limited column number in JSON stats (
#44233
)
Made load resource count n-gram index (
#44237
)
Deduced metric type from non-empty search results (
#44222
)
Fixed multi-segment write only writing one segment (
#44256
)
Fixed merge sort out of range (
#44230
)
Added UTF-8 check before executing BM25 function (
#44220
)
Retried old session if it exists (
#44208
)
Added Kafka buffer size limit to prevent datanode OOM (
#44106
)
Fixed panic by extending lock guarding range (
#44130
)
Fixed growing segments not being flushed on schema change (
#44412
)
[StorageV2] Handled IO errors (
#44255
)
Prevented panic if Tantivy index path does not exist (
#44135
)
v2.6.1
Release date: September 3, 2025
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.1
2.6.1
2.6.0
2.6.3
2.6.1
We are excited to announce the release of Milvus 2.6.1! This version builds upon the major architectural advancements of previous releases, delivering critical enhancements focused on production stability, performance, and operational robustness. This release addresses key community feedback and strengthens the system for large-scale deployments. We strongly encourage all users to upgrade to benefit from a more stable, performant, and reliable system.
Improvements
Supports POSIX-compatible file systems for remote storage (
#43944
)
Introduces model-based rerankers (
#43270
)
Optimizes the performance of comparison expressions on primary key fields (
#43154
)
Collects doc_id from posting list directly to accelerate text match (
#43899
)
Optimizes query performance by converting multiple != conditions into a single NOT IN clause (
#43690
)
Enhances resource management for the caching layer during segment loading (
#43846
)
Improves memory estimation for interim indexes during data loading (
#44104
)
Makes the build ratio for interim indexes configurable (
#43939
)
Adds a configurable write rate limit to the disk writer (
#43912
)
SegCore parameters can now be updated dynamically without restarting the Milvus service (
#43231
)
Adds unified gRPC latency metrics for better observability (
#44089
)
Includes client request timestamps in gRPC headers to simplify debugging (
#44059
)
Supports trace log level for segcore (
#44003
)
Adds a configurable switch to adjust consistency guarantees for higher availability (
#43874
)
Implements a robust rewatch mechanism to handle etcd connection failures (
#43829
)
Improves the internal node health check logic (
#43768
)
Optimizes metadata access when listing collections (
#43902
)
Upgrades the Pulsar client to v0.15.1 official version and adds more logging (
#43913
)
Upgrades aws-sdk from 1.9.234 to 1.11.352 (
#43916
)
Supports dynamic interval updates for ticker components (
#43865
)
Improves auto-detection of ARM SVE instruction sets for bitset operations (
#43833
)
Improves the error message when a text or phrase match fails (
#43366
)
Improves the error message for vector dimension mismatches (
#43835
)
Improves error reporting for append timeouts when the object store is unavailable (
#43926
)
Bug fixes
Fixes a potential Out-Of-Memory (OOM) issue during Parquet file imports (
#43756
)
Fixes an issue where standby nodes could not recover if their lease expired (
#44112
)
Handles compaction retry state correctly (
#44119
)
Fixes a potential deadlock between continuous read requests and index loading that could prevent index loading (
#43937
)
Fixes a bug that could cause data deletions to fail in high-concurrency scenarios (
#43831
)
Fixes a potential race condition when loading text and JSON indexes (
#43811
)
Fixes a node status inconsistency that could occur after a QueryCoord restart (
#43941
)
Ensures that a “dirty” QueryNode is properly cleaned up after a restart (
#43909
)
Fixes an issue where the retry state was not handled correctly for requests with non-empty payloads (
#44068
)
Fixes an issue where the bulk writer v2 did not use the correct bucket name (
#44083
)
Enhances security by hiding sensitive items from the RESTful get_configs endpoint (
#44057
)
Ensures that object uploads for woodpecker are idempotent during timeout retries (
#43947
)
Disallows importing null elements in array fields from Parquet files (
#43964
)
Fixes a bug where the proxy cache was not invalidated after creating a collection alias (
#43854
)
Improves the internal service discovery mechanism for streaming nodes (
#44033
)
Fixes resource group logic to correctly filter streaming nodes (
#43984
)
Adds the databaseName label to metrics to prevent naming conflicts in multi-database environments (
#43808
)
Fixes a logic error in internal task state handling (
#43777
)
Optimizes the initialization timing of the internal metrics to avoid potential panic (
#43773
)
Fixes a rare potential crash in the internal HTTP server (
#43799
)
v2.6.0
Release date: August 6, 2025
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.0
2.6.0
2.6.0
2.6.1
2.6.0
Milvus 2.6.0 is officially released! Building upon the architectural foundation laid in
2.6.0-rc1
, this production-ready version addresses numerous stability and performance issues while introducing powerful new capabilities including Storage Format V2, advanced JSON processing, and enhanced search features. With extensive bug fixes and optimizations based on community feedback during the RC phase, Milvus 2.6.0 is ready for you to explore and adopt.
Direct upgrade from pre-2.6.0 versions is not supported due to architectural changes. Please follow our
upgrade guide
.
What’s new in 2.6.0 (since RC)
Optimized storage format v2
To address the challenges of mixed scalar and vector data storage, especially point lookups on unstructured data, Milvus 2.6 introduces Storage Format V2. This new adaptive columnar storage format adopts a “narrow column merging + wide column independence” layout strategy, fundamentally solving the performance bottlenecks when handling point lookups and small-batch retrievals in vector databases.
The new format now supports efficient random access without I/O amplification and achieves up to 100x performance gains compared to the vanilla Parquet format adopted previously, making it ideal for AI workloads requiring both analytical processing and precise vector retrieval. Additionally, it can reduce file count by up to 98% for typical workloads. Memory consumption for major compaction is reduced by 300%, and I/O operations are optimized by up to 80% for reads and more than 600% for writes.
JSON flat index (beta)
Milvus 2.6 introduces JSON Flat Index to handle highly dynamic JSON schemas. Unlike JSON Path Index which requires pre-declaring specific paths and their expected types, JSON Flat Index automatically discovers and indexes all nested structures under a given path. When indexing a JSON field, it recursively flattens the entire subtree, creating inverted index entries for every path-value pair it encounters, regardless of depth or type.
This automatic flattening makes JSON Flat Index ideal for evolving schemas where new fields appear without warning. For instance, if you index a “metadata” field, the system will automatically handle new nested fields like “metadata.version2.features.experimental” as they appear in incoming data, without requiring new index configuration.
Core 2.6.0 features recall
For detailed information about architecture changes and features introduced in 2.6.0-RC, see
2.6.0-rc1 Release Note
.
Architecture simplification
Streaming Node (GA) - Centralized WAL management
Native WAL with Woodpecker - Removed Kafka/Pulsar dependency
Unified coordinators (MixCoord); Merged IndexNode and DataNode - Reduced component complexity
Search & analytics
RaBitQ 1-bit quantization with high recall
Phrase matching
MinHash LSH for deduplication
Time-aware ranking functions
Developer experience
Embedding functions for “data-in, data-out” workflow
Online schema evolution
INT8 vector support
Enhanced tokenizers for global language support
Cache layer with lazy loading - Process datasets larger than memory
v2.6.0-rc1
Release date: June 18, 2025
Milvus Version
Python SDK Version
Node.js SDK Version
Java SDK Version
Go SDK Version
2.6.0-rc1
2.6.0b0
2.6.0-rc1
2.6.0
2.6.0-rc.1
Milvus 2.6.0-rc1 introduces a simplified, cloud-native architecture designed to improve operational efficiency, resource utilization, and total cost of ownership by reducing deployment complexity. This release adds new functionalities focused on performance, search, and development. Key features include high-precision 1-bit quantization (RaBitQ) and a dynamic cache layer for performance gains, near-duplicate detection with MinHash and precise phrase matching for advanced search, and automated embedding functions with online schema modification to enhance the developer’s experience.
This is a pre-release version of Milvus 2.6.0. To try out the latest features, install this version as a fresh deployment. Upgrading from Milvus v2.5.x or earlier to 2.6.0-rc1 is not supported.
Architecture Changes
Since 2.6, Milvus introduces significant architectural changes aimed at improving performance, scalability, and ease of use. For more information, refer to
Milvus Architecture Overview
.
Streaming Node (GA)
In previous versions, streaming data was written to the WAL by the Proxy, and read by the QueryNode and DataNode. This architecture made it difficult to achieve consensus on the write side, requiring complex logic on the read side. Additionally, the query delegator was located in the QueryNode, which hindered scalability. Milvus 2.5.0 introduced the Streaming Node, which becomes GA in version 2.6.0. This component is now responsible for all shard-level WAL read/write operations and also serves as the query delegator, resolving the aforementioned issues and enabling new optimizations.
Important Upgrade Notice
: Streaming Node is a significant architectural change, so a direct upgrade to Milvus 2.6.0-rc1 from previous versions is not supported.
Woodpecker Native WAL
Milvus previously relied on external systems like Kafka or Pulsar for its WAL. While functional, these systems added significant operational complexity and resource overhead, particularly for small to medium-sized deployments. In Milvus 2.6, these are replaced by Woodpecker, a purpose-built, cloud-native WAL system. Woodpecker is designed for object storage, supporting both local and object storage based zero-disk modes, simplifying operations while improving performance and scalability.
DataNode and IndexNode Merge
In Milvus 2.6, tasks such as compaction, bulk import, statistics collection, and index building are now managed by a unified scheduler. The data persistence function previously handled by the DataNode has been moved to the Streaming Node. To simplify deployment and maintenance, the IndexNode and DataNode have been merged into a single DataNode component. This consolidated node now executes all these critical tasks, reducing operational complexity and optimizing resource utilization.
Coordinator Merge into MixCoord
The previous design with separate RootCoord, QueryCoord, and DataCoord modules introduced complexity in inter-module communication. To simplify the system design, these components have been merged into a single, unified coordinator called MixCoord. This consolidation reduces the complexity of distributed programming by replacing network-based communication with internal function calls, resulting in more efficient system operation and simplified development and maintenance.
Key Features
RaBitQ 1-bit Quantization
To handle large-scale datasets, 1-bit quantization is an effective technique for improving resource utilization and search performance. However, traditional methods can negatively impact recall. In collaboration with the original research authors, Milvus 2.6 introduces RaBitQ, a 1-bit quantization solution that maintains high recall accuracy while delivering the resource and performance benefits of 1-bit compression.
For more information, refer to
IVF_RABITQ
.
JSON Capability Enhancement
Milvus 2.6 enhances its support for the JSON data type with the following improvements:
Performance
: JSON Path Indexing is now officially supported, allowing the creation of inverted indexes on specific paths within JSON objects (e.g.,
meta.user.location
). This avoids full object scans and improves the latency of queries with complex filters.
Functionality
: To support more complex filtering logic, this release adds support for
JSON_CONTAINS
,
JSON_EXISTS
,
IS NULL
, and
CAST
functions.
Looking ahead, our work on JSON support continues. We are excited to preview that upcoming official releases will feature even more powerful capabilities, such as
JSON shredding
and a
JSON FLAT Index
, designed to dramatically improve performance on highly nested JSON data.
Analyzer/Tokenizer Function Enhancement
This release significantly enhances text processing capabilities with several updates to the Analyzer and Tokenizer:
A new
Run Analyzer
syntax is available to validate tokenizer configurations.
The
Lindera tokenizer
is integrated for improved support of Asian languages such as Japanese and Korean.
Row-level tokenizer selection is now supported, with the general-purpose
ICU tokenizer
available as a fallback for multilingual scenarios.
Data-in, Data-Out with Embedding Functions
Milvus 2.6 introduces a “Data-in, Data-Out” capability that simplifies AI application development by integrating directly with third-party embedding models (e.g., from OpenAI, AWS Bedrock, Google Vertex AI, Hugging Face). Users can now insert and query using raw text data, and Milvus will automatically call the specified model service to convert the text into vectors in real-time. This removes the need for a separate vector conversion pipeline.
For more information, refer to
Embedding Function Overview
.
Phrase Match
Phrase Match is a text search feature that returns results only when the exact sequence of words in a query appears consecutively and in the correct order within a document.
Key Characteristics
:
Order-sensitive: The words must appear in the same order as in the query.
Consecutive match: The words must appear right next to each other, unless a slop value is used.
Slop (optional): A tunable parameter that allows for a small number of intervening words, enabling fuzzy phrase matching.
For more information, refer to
Phrase Match
.
MinHash LSH Index (Beta)
To address the need for data deduplication in model training, Milvus 2.6 adds support for MINHASH_LSH indexes. This feature provides a computationally efficient and scalable method for estimating Jaccard similarity between documents to identify near-duplicates. Users can generate MinHash signatures for their text documents during preprocessing and use the MINHASH_LSH index in Milvus to efficiently find similar content in large-scale datasets, improving data cleaning and model quality.
Time-Aware Decay Functions
Milvus 2.6 introduces time-aware decay functions to address scenarios where information value changes over time. During result re-ranking, users can apply exponential, Gaussian, or linear decay functions based on a timestamp field to adjust a document’s relevance score. This ensures that more recent content can be prioritized, which is critical for applications like news feeds, e-commerce, and an AI agent’s memory.
For more information, refer to
Decay Ranker Overview
.
Add Field for Online Schema Evolution
To provide greater schema flexibility, Milvus 2.6 now supports adding a new scalar field to an existing collection’s schema online. This avoids the need to create a new collection and perform a disruptive data migration when application requirements change.
For more information, refer to
Add Fields to an Existing Collection
.
INT8 Vector Support
In response to the growing use of quantized models that produce 8-bit integer embeddings, Milvus 2.6 adds native data type support for INT8 vectors. This allows users to ingest these vectors directly without de-quantization, saving computation, network bandwidth, and storage costs. This feature is initially supported for HNSW-family indexes.
For more information, refer to
Dense Vector
.