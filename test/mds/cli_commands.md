Milvus_CLI Command Reference
Milvus Command-Line Interface (CLI) is a command-line tool that supports database connection, data operations, and import and export of data.
This topic introduces all supported commands and the corresponding options. Some examples are also included for your reference.
Command Groups
Milvus CLI commands are organized into the following groups:
create
: Create collection, database, partition, user, role, alias, index, privilege_group, or resource_group
delete
: Delete collection, database, partition, alias, user, role, index, entities, IDs, privilege_group, resource_group, connection_history, or collection_properties
list
: List collections, databases, partitions, users, roles, grants, indexes, aliases, connections, connection_history, privilege_groups, resource_groups, or bulk_insert_tasks
show
: Show collection, collection_stats, database, partition, partition_stats, index, index_progress, loading_progress, load_state, flush_state, compaction_state, compaction_plans, replicas, query_segment_info, role, user, alias, output, resource_group, or bulk_insert_state
grant
: Grant role, privilege, or privilege_group
revoke
: Revoke role, privilege, or privilege_group
load
: Load collection or partition
release
: Release collection or partition
use
: Use database
rename
: Rename collection
insert
: Insert entities (file or row)
upsert
: Upsert entities (file or row)
set
: Set output format
alter
: Alter database, collection_properties, or collection_field
update
: Update password or resource_group
clear
Clears the screen.
Syntax
clear
connect
Connects to Milvus.
Syntax
connect [-uri (text)] [-t (text)] [-tls (0|1|2)] [-cert (text)] [--save-as (text)]
Options
Option
Full name
Description
-uri
–uri
(Optional) The uri name. The default is "http://127.0.0.1:19530". Can also be set via
ZILLIZ_URI
environment variable.
-t
–token
(Optional) The zilliz cloud apikey or
username:password
. Can also be set via
ZILLIZ_TOKEN
environment variable.
-tls
–tlsmode
(Optional) Set TLS mode: 0 (No encryption), 1 (One-way encryption), 2 (Two-way encryption). Default is 0.
-cert
–cert
(Optional) Path to the client certificate file. Works with one-way encryption.
–save-as
n/a
(Optional) Save connection with custom alias for later use.
–help
n/a
Displays help for using the command.
Examples
milvus_cli > connect -uri http://127.0.0.1:19530

milvus_cli > connect -uri http://192.168.1.100:19530 -t root:milvus

milvus_cli > connect -uri https://xxx.zillizcloud.com -t <api_key>
disconnect
Disconnects from Milvus.
Syntax
disconnect
create database
Creates a database in Milvus.
Syntax
create database -db (text)
Options
Option
Full name
Description
-db
–db_name
[Required] The database name in milvus.
–help
n/a
Displays help for using the command.
Example
milvus_cli > create database -db testdb
use database
Uses a database in Milvus.
Syntax
use database -db (text)
Options
Option
Full name
Description
-db
–db_name
[Required] The database name in milvus.
–help
n/a
Displays help for using the command.
Example
milvus_cli > use database -db testdb
list databases
Lists all databases in Milvus.
Syntax
list databases
show database
Shows details and properties of a database.
Syntax
show database [-db (text)]
Options
Option
Full name
Description
-db
–db_name
(Optional) The database name. Defaults to current.
–help
n/a
Displays help for using the command.
alter database
Alters database properties.
Syntax
alter database -db (text)
Options
Option
Full name
Description
-db
–db_name
[Required] The database name in milvus.
–help
n/a
Displays help for using the command.
Interactive Example
milvus_cli > alter database -db testdb

Property key: collection.ttl.seconds
Property value: 86400
delete database
Deletes a database in Milvus.
Syntax
delete database -db (text) [--yes]
Options
Option
Full name
Description
-db
–db_name
[Required] The database name in milvus.
–yes
-y
(Optional) Skip confirmation prompt.
–help
n/a
Displays help for using the command.
Example
milvus_cli > delete database -db testdb

Warning! You are trying to delete the database. This action cannot be undone!
Do you want to continue? [y/N]: y
create collection
Creates a collection.
Syntax
create collection [--schema-file (text)]
Options
Option
Full name
Description
–schema-file
–schema-file
(Optional) Path to JSON file with schema definition.
–help
n/a
Displays help for using the command.
Interactive Example
milvus_cli > create collection

Please input collection name: car
Please input auto id [False]: False
Please input description []: car collection
Is support dynamic field [False]: False
Please input consistency level(Strong(0),Bounded(1), Session(2), and Eventually(3)) [1]: 1
Please input shards number [1]: 1

Field name: id
Field type (INT64, VARCHAR, FLOAT_VECTOR, etc.): INT64
Field description []: primary key
Is id the primary key? [y/N]: y

Field name: vector
Field type (INT64, VARCHAR, FLOAT_VECTOR, etc.): FLOAT_VECTOR
Field description []: vector field
Dimension: 128

Field name:

Do you want to add embedding function? [y/N]: n
list collections
Lists all collections in the current database.
Syntax
list collections
show collection
Shows the detailed information of a collection.
Syntax
show collection -c (text)
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
–help
n/a
Displays help for using the command.
show collection_stats
Shows collection statistics.
Syntax
show collection_stats -c (text)
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
–help
n/a
Displays help for using the command.
rename collection
Renames a collection.
Syntax
rename collection -old (text) -new (text)
Options
Option
Full name
Description
-old
–old-collection-name
[Required] The old collection name.
-new
–new-collection-name
[Required] The new collection name.
–help
n/a
Displays help for using the command.
delete collection
Deletes a collection.
Syntax
delete collection -c (text) [--yes]
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
–yes
-y
(Optional) Skip confirmation prompt.
–help
n/a
Displays help for using the command.
Example
milvus_cli > delete collection -c car

Warning! You are trying to delete the collection. This action cannot be undone!
Do you want to continue? [y/N]: y
load collection
Loads a collection into RAM.
Syntax
load collection -c (text)
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
–help
n/a
Displays help for using the command.
release collection
Releases a collection from RAM.
Syntax
release collection -c (text)
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
–help
n/a
Displays help for using the command.
truncate
Removes all data from a collection but keeps the schema.
Syntax
truncate -c (text) [--yes]
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
–yes
-y
(Optional) Skip confirmation prompt.
–help
n/a
Displays help for using the command.
Example
milvus_cli > truncate -c car

Warning!
You are trying to remove all data in the collection. This action cannot be undone!
Do you want to continue? [y/N]: y
flush
Flushes collection data to storage.
Syntax
flush -c (text) [-t (number)]
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
-t
–timeout
(Optional) Timeout in seconds.
–help
n/a
Displays help for using the command.
flush_all
Flushes all collections to storage.
Syntax
flush_all [-t (number)]
Options
Option
Full name
Description
-t
–timeout
(Optional) Timeout in seconds.
–help
n/a
Displays help for using the command.
show flush_state
Shows flush state for a collection.
Syntax
show flush_state -c (text)
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
–help
n/a
Displays help for using the command.
compact
Compacts a collection to merge small segments and remove deleted data.
Syntax
compact -c (text) [-t (number)]
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
-t
–timeout
(Optional) Timeout in seconds.
–help
n/a
Displays help for using the command.
show compaction_state
Shows compaction state.
Syntax
show compaction_state -id (number)
Options
Option
Full name
Description
-id
–compaction-id
[Required] The compaction ID.
–help
n/a
Displays help for using the command.
show compaction_plans
Shows compaction plans.
Syntax
show compaction_plans -c (text) -id (number)
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
-id
–compaction-id
[Required] The compaction ID.
–help
n/a
Displays help for using the command.
show loading_progress
Displays the progress of loading a collection.
Syntax
show loading_progress -c (text)
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
–help
n/a
Displays help for using the command.
show load_state
Shows the load state of a collection or partition.
Syntax
show load_state -c (text) [-p (text)]
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
-p
–partition
(Optional) The name of the partition.
–help
n/a
Displays help for using the command.
show replicas
Shows replicas information for a collection.
Syntax
show replicas -c (text)
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
–help
n/a
Displays help for using the command.
show query_segment_info
Shows query segment information for a collection.
Syntax
show query_segment_info -c (text)
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
–help
n/a
Displays help for using the command.
alter collection_properties
Alters collection properties like TTL, mmap, etc.
Syntax
alter collection_properties -c (text)
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
–help
n/a
Displays help for using the command.
Interactive Example
milvus_cli > alter collection_properties -c car

Property key: collection.ttl.seconds
Property value: 86400
delete collection_properties
Drops collection properties by key.
Syntax
delete collection_properties -c (text) -k (text)
Options
Option
Full name
Description
-c
–collection-name
[Required] The target collection.
-k
–property-key
[Required] The property key to delete.
–help
n/a
Displays help for using the command.
alter collection_field
Alters collection field properties.
Syntax
alter collection_field -c (text) -f (text)
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
-f
–field-name
[Required] The name of the field to alter.
–help
n/a
Displays help for using the command.
Interactive Example
milvus_cli > alter collection_field -c car -f color

Property key: max_length
Property value: 256
create partition
Creates a partition.
Syntax
create partition -c (text) -p (text) [-d (text)]
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
-p
–partition
The partition name.
-d
–description
(Optional) The description of the partition.
–help
n/a
Displays help for using the command.
Example
milvus_cli > create partition -c car -p new_partition -d test_add_partition
list partitions
Lists all partitions of a collection.
Syntax
list partitions -c (text)
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
–help
n/a
Displays help for using the command.
show partition
Shows the detailed information of a partition.
Syntax
show partition -c (text) -p (text)
Options
Option
Full name
Description
-c
–collection-name
The name of the collection that the partition belongs to.
-p
–partition
The name of the partition.
–help
n/a
Displays help for using the command.
show partition_stats
Shows partition statistics.
Syntax
show partition_stats -c (text) -p (text)
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
-p
–partition
[Required] The name of the partition.
–help
n/a
Displays help for using the command.
delete partition
Deletes a partition.
Syntax
delete partition -c (text) -p (text)
Options
Option
Full name
Description
-c
–collection-name
The name of the collection that the partition to be deleted belongs to.
-p
–partition
The name of the partition to be deleted.
–help
n/a
Displays help for using the command.
load partition
Loads a partition into RAM.
Syntax
load partition -c (text) -p (text)
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
-p
–partition
The name of the partition.
–help
n/a
Displays help for using the command.
release partition
Releases a partition from RAM.
Syntax
release partition -c (text) -p (text)
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
-p
–partition
The name of the partition.
–help
n/a
Displays help for using the command.
create index
Creates an index for a field.
Syntax
create index
Interactive Example
milvus_cli > create index

Collection name (car, car2): car
The name of the field to create an index for (vector): vector
Index name: vectorIndex
Index type (FLAT, IVF_FLAT, IVF_SQ8, IVF_PQ, HNSW, AUTOINDEX, DISKANN, GPU_IVF_FLAT, GPU_IVF_PQ, SPARSE_INVERTED_INDEX, SCANN, STL_SORT, Trie, INVERTED): IVF_FLAT
Vector Index metric type (L2, IP, HAMMING, TANIMOTO, COSINE): L2
Index params nlist: 2
Timeout []:
list indexes
Lists all indexes for a collection.
Syntax
list indexes -c (text)
Options
Option
Full name
Description
-c
–collection
The name of the collection.
–help
n/a
Displays help for using the command.
show index
Shows the detailed information of an index.
Syntax
show index -c (text) -in (text)
Options
Option
Full name
Description
-c
–collection
The name of the collection.
-in
–index-name
The name of the index.
–help
n/a
Displays help for using the command.
show index_progress
Shows the progress of entity indexing.
Syntax
show index_progress -c (text) [-in (text)]
Options
Option
Full name
Description
-c
–collection
The name of the collection.
-in
–index-name
(Optional) The name of the index.
–help
n/a
Displays help for using the command.
delete index
Deletes an index.
Syntax
delete index -c (text) -in (text)
Options
Option
Full name
Description
-c
–collection
The name of the collection.
-in
–index-name
The name of the index.
–help
n/a
Displays help for using the command.
wait_for_index
Waits for index building to complete.
Syntax
wait_for_index -c (text) [-in (text)] [-t (number)]
Options
Option
Full name
Description
-c
–collection
[Required] The name of the collection.
-in
–index-name
(Optional) The name of the index.
-t
–timeout
(Optional) Timeout in seconds.
–help
n/a
Displays help for using the command.
insert file
Imports data from a CSV file into a collection.
Syntax
insert file -c (text) [-p (text)] [-t (number)] <file_path>
Options
Option
Full name
Description
-c
–collection-name
The name of the collection that the data are inserted into.
-p
–partition
(Optional) The partition name. Default is "_default".
-t
–timeout
(Optional) Timeout in seconds.
–help
n/a
Displays help for using the command.
Example
milvus_cli > insert file -c car 'examples/import_csv/vectors.csv'

Reading csv file...  [####################################]  100%

Column names are ['vector', 'color', 'brand']

Processed 50001 lines.

Inserting ...

Insert successfully.
--------------------------  ------------------
Total insert entities:                   50000
Total collection entities:              150000
Milvus timestamp:           428849214449254403
--------------------------  ------------------
insert row
Inserts a row of data into a collection.
Syntax
insert row
Interactive Example
milvus_cli > insert row

Collection name: car
Partition name [_default]: _default
Enter value for id (INT64): 1
Enter value for vector (FLOAT_VECTOR): [1.0, 2.0, 3.0]
Enter value for color (INT64): 100
Enter value for brand (VARCHAR): Toyota

Inserted successfully.
upsert file
Upserts data from a CSV file into a collection.
Syntax
upsert file -c (text) [-p (text)] [-t (number)] <file_path>
Options
Option
Full name
Description
-c
–collection-name
The name of the collection to upsert into.
-p
–partition
(Optional) The partition name. Default is "_default".
-t
–timeout
(Optional) Timeout in seconds.
–help
n/a
Displays help for using the command.
upsert row
Upserts a row of data into a collection.
Syntax
upsert row
Interactive Example
milvus_cli > upsert row

Collection name: car
Partition name [_default]: _default
Enter value for id (INT64): 1
Enter value for vector (FLOAT_VECTOR): [1.0, 2.0, 3.0]
Enter value for color (INT64): 200
Enter value for brand (VARCHAR): Honda

Upserted successfully.
delete entities
Deletes entities using a filter expression.
Syntax
delete entities -c (text) [-p (text)]
Options
Option
Full name
Description
-c
–collection-name
The name of the collection that entities to be deleted belongs to.
-p
–partition
(Optional) The name of the partition.
–help
n/a
Displays help for using the command.
Interactive Example
milvus_cli > delete entities -c car

The expression to specify entities to be deleted, such as "film_id in [ 0, 1 ]": film_id in [ 0, 1 ]

Warning! You are trying to delete the entities of collection. This action cannot be undone!
Do you want to continue? [y/N]: y
delete ids
Deletes entities by IDs.
Syntax
delete ids -c (text) [-p (text)]
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
-p
–partition
(Optional) The name of the partition.
–help
n/a
Displays help for using the command.
Interactive Example
milvus_cli > delete ids -c car

IDs to delete (comma-separated): 1, 2, 3
get
Gets entities by IDs.
Syntax
get
Interactive Example
milvus_cli > get

Collection name: car
IDs (comma-separated): 1, 2, 3
Output fields (comma-separated, or * for all) []: color, brand
query
Shows query results that match all the criteria you enter.
Syntax
query
Interactive Example
milvus_cli > query

Collection name: car

The query expression: id in [ 428960801420883491, 428960801420883492 ]

Name of partitions that contain entities(split by "," if multiple) []: default

A list of fields to return(split by "," if multiple) []: color, brand

timeout []:

Guarantee timestamp. This instructs Milvus to see all operations performed before a provided timestamp. [0]:

Graceful time. Only used in bounded consistency level. [5]:
search
Performs a vector similarity search.
Syntax
search
Interactive Example
milvus_cli > search

Collection name (car, test_collection): car

The vectors of search data: examples/import_csv/search_vectors.csv

The vector field used to search of collection (vector): vector

Search parameter nprobe's value: 10

The max number of returned record, also known as topk: 2

The boolean expression used to filter attribute []: id > 0

The names of partitions to search (split by "," if multiple) ['_default'] []: _default

timeout []:

Guarantee Timestamp [0]:
hybrid_search
Performs a hybrid search (multi-vector search) with reranking.
Syntax
hybrid_search
Interactive Example
milvus_cli > hybrid_search

Collection name: car

Enter search requests (one per line, empty line to finish):
  Vector field, search vector, metric type, top K, filter expression...

Rerank strategy (rrf, weighted, etc.): rrf

Output fields (comma-separated) []: color, brand
query_iterator
Queries entities with iterator for large result sets.
Syntax
query_iterator
Interactive Example
milvus_cli > query_iterator

Collection name: car
Filter expression []: id > 0
Output fields (comma-separated, or * for all) []: color, brand
Batch size [1000]: 1000
Limit [10]: 100
search_iterator
Searches with iterator for large result sets.
Syntax
search_iterator
Interactive Example
milvus_cli > search_iterator

Collection name: car
Vector field name: vector
Search vector (comma-separated floats): 1.0, 2.0, 3.0, ...
Batch size [1000]: 1000
Limit [10]: 100
Filter expression []:
Output fields (comma-separated) []: color, brand
bulk_insert
Bulk inserts data from remote storage (S3, MinIO, etc.).
Syntax
bulk_insert -c (text) [-p (text)] -f (text)
Options
Option
Full name
Description
-c
–collection-name
[Required] The name of the collection.
-p
–partition
(Optional) The partition name.
-f
–files
[Required] File paths (comma separated).
–help
n/a
Displays help for using the command.
show bulk_insert_state
Shows bulk insert task state.
Syntax
show bulk_insert_state -id (number)
Options
Option
Full name
Description
-id
–task-id
[Required] The bulk insert task ID.
–help
n/a
Displays help for using the command.
list bulk_insert_tasks
Lists bulk insert tasks.
Syntax
list bulk_insert_tasks [-l (number)] [-c (text)]
Options
Option
Full name
Description
-l
–limit
(Optional) Maximum number of tasks to return.
-c
–collection-name
(Optional) Filter by collection name.
–help
n/a
Displays help for using the command.
create user
Creates a user in Milvus.
Syntax
create user -u (text) -p (text)
Options
Option
Full name
Description
-u
–username
The username.
-p
–password
The password.
–help
n/a
Displays help for using the command.
Example
milvus_cli > create user -u zilliz -p zilliz
list users
Lists all users.
Syntax
list users
show user
Shows user details and assigned roles.
Syntax
show user -u (text)
Options
Option
Full name
Description
-u
–username
[Required] The username to describe.
–help
n/a
Displays help for using the command.
delete user
Deletes a user.
Syntax
delete user -u (text)
Options
Option
Full name
Description
-u
–username
The username.
–help
n/a
Displays help for using the command.
update password
Updates a user’s password.
Syntax
update password -u (text)
Options
Option
Full name
Description
-u
–username
[Required] The username to update.
–help
n/a
Displays help for using the command.
Interactive Example
milvus_cli > update password -u zilliz

Old password:
New password:
Confirm new password:
create role
Creates a role in Milvus.
Syntax
create role -r (text)
Options
Option
Full name
Description
-r
–roleName
The role name.
–help
n/a
Displays help for using the command.
list roles
Lists all roles.
Syntax
list roles
show role
Shows role details and granted privileges.
Syntax
show role -r (text)
Options
Option
Full name
Description
-r
–roleName
[Required] The role name.
–help
n/a
Displays help for using the command.
delete role
Deletes a role.
Syntax
delete role -r (text)
Options
Option
Full name
Description
-r
–roleName
The role name.
–help
n/a
Displays help for using the command.
grant role
Assigns a user to a role.
Syntax
grant role -r (text) -u (text)
Options
Option
Full name
Description
-r
–roleName
The role name.
-u
–username
The username.
–help
n/a
Displays help for using the command.
revoke role
Removes a user from a role.
Syntax
revoke role -r (text) -u (text)
Options
Option
Full name
Description
-r
–roleName
The role name.
-u
–username
The username.
–help
n/a
Displays help for using the command.
grant privilege
Grants a privilege to a role.
Syntax
grant privilege
Interactive Example
milvus_cli > grant privilege

Role name: role1
The type of object for which the privilege is to be assigned. (Global, Collection, User): Collection
The name of the object to control access for: object1
The name of the privilege to assign. (CreateCollection, DropCollection, etc.): CreateCollection
The name of the database to which the object belongs. [default]: default
revoke privilege
Revokes a privilege from a role.
Syntax
revoke privilege
Interactive Example
milvus_cli > revoke privilege

Role name: role1
The type of object for which the privilege is to be assigned. (Global, Collection, User): Collection
The name of the object to control access for: object1
The name of the privilege to assign. (CreateCollection, DropCollection, etc.): CreateCollection
The name of the database to which the object belongs. [default]: default
list grants
Lists grants for a role.
Syntax
list grants -r (text) -o (text) -t (text)
Options
Option
Full name
Description
-r
–roleName
The role name.
-o
–objectName
The object name.
-t
–objectType
Global, Collection, or User.
–help
n/a
Displays help for using the command.
create alias
Specifies an alias for a collection.
A collection can have multiple aliases. However, an alias corresponds to a maximum of one collection.
Syntax
create alias -c (text) -a (text) [-A]
Options
Option
Full name
Description
-c
–collection-name
The name of the collection.
-a
–alias-name
The alias.
-A
–alter
(Optional) Flag to transfer the alias to a specified collection.
–help
n/a
Displays help for using the command.
Example
milvus_cli > create alias -c car -a carAlias1
list aliases
Lists aliases in the database.
Syntax
list aliases [-c (text)]
Options
Option
Full name
Description
-c
–collection-name
(Optional) Filter aliases by collection.
–help
n/a
Displays help for using the command.
show alias
Shows details of an alias.
Syntax
show alias -a (text)
Options
Option
Full name
Description
-a
–alias-name
[Required] The alias name.
–help
n/a
Displays help for using the command.
delete alias
Deletes an alias.
Syntax
delete alias -a (text)
Options
Option
Full name
Description
-a
–alias-name
The alias.
–help
n/a
Displays help for using the command.
create privilege_group
Creates a new privilege group.
Syntax
create privilege_group -n (text)
Options
Option
Full name
Description
-n
–name
[Required] The privilege group name.
–help
n/a
Displays help for using the command.
list privilege_groups
Lists all privilege groups.
Syntax
list privilege_groups
grant privilege_group
Adds privileges to a privilege group.
Syntax
grant privilege_group -n (text) -p (text)
Options
Option
Full name
Description
-n
–name
[Required] The privilege group name.
-p
–privileges
[Required] Comma-separated list of privileges.
–help
n/a
Displays help for using the command.
Example
milvus_cli > grant privilege_group -n my_group -p CreateCollection,DropCollection
revoke privilege_group
Removes privileges from a privilege group.
Syntax
revoke privilege_group -n (text) -p (text)
Options
Option
Full name
Description
-n
–name
[Required] The privilege group name.
-p
–privileges
[Required] Comma-separated list of privileges.
–help
n/a
Displays help for using the command.
delete privilege_group
Deletes a privilege group.
Syntax
delete privilege_group -n (text) [--yes]
Options
Option
Full name
Description
-n
–name
[Required] The privilege group name.
–yes
-y
(Optional) Skip confirmation prompt.
–help
n/a
Displays help for using the command.
create resource_group
Creates a new resource group.
Syntax
create resource_group -n (text)
Options
Option
Full name
Description
-n
–name
[Required] The resource group name.
–help
n/a
Displays help for using the command.
Interactive Example
milvus_cli > create resource_group -n my_rg

Configure node limits? [y/N]: y
requests.node_num [0]: 1
limits.node_num [0]: 3
list resource_groups
Lists all resource groups.
Syntax
list resource_groups
show resource_group
Shows resource group details.
Syntax
show resource_group -n (text)
Options
Option
Full name
Description
-n
–name
[Required] The resource group name.
–help
n/a
Displays help for using the command.
update resource_group
Updates resource group configuration.
Syntax
update resource_group -n (text)
Options
Option
Full name
Description
-n
–name
[Required] The resource group name.
–help
n/a
Displays help for using the command.
Interactive Example
milvus_cli > update resource_group -n my_rg

requests.node_num [current]: 2
limits.node_num [current]: 5
delete resource_group
Deletes a resource group.
Syntax
delete resource_group -n (text)
Options
Option
Full name
Description
-n
–name
[Required] The resource group name.
–help
n/a
Displays help for using the command.
transfer replica
Transfers replicas between resource groups.
Syntax
transfer replica
Interactive Example
milvus_cli > transfer replica

Source resource group: __default_resource_group
Target resource group: my_rg
Collection name: car
Number of replicas to transfer: 1
list connections
Lists all Milvus connections.
Syntax
list connections
list connection_history
Lists saved connection history.
Syntax
list connection_history
delete connection_history
Deletes a saved connection from history.
Syntax
delete connection_history -uri (text)
Options
Option
Full name
Description
-uri
–uri
[Required] URI of the connection to delete.
–help
n/a
Displays help for using the command.
show output
Shows the current output format setting.
Syntax
show output
set output
Sets the global output format for CLI results.
Syntax
set output (table|json|csv)
Example
milvus_cli > set output json
history
Shows or clears command history.
Syntax
history [clear]
Examples
milvus_cli > history

milvus_cli > history clear
version
Shows the version of Milvus_CLI.
Syntax
version
You can also check the version of Milvus_CLI in a shell as shown in the following example. In this case,
milvus_cli --version
acts as a command.
Example
$
milvus_cli --version
Milvus_CLI v1.2.1
exit
Closes the command line window.
Syntax
exit
help
Displays help for using a command.
Syntax
help <command>
Commands
Command
Description
alter
Alter database, collection properties, or collection field.
clear
Clears the screen.
compact
Compact a collection.
connect
Connects to Milvus.
create
Create collection, database, partition, user, role, alias, index, and more.
delete
Delete collection, database, partition, alias, user, role, index, and more.
exit
Closes the command line window.
flush
Flush collection data to storage.
get
Get entities by IDs.
grant
Grant role, privilege, or privilege_group.
help
Displays help for using a command.
history
Show or clear command history.
insert
Import data into a collection.
list
List collections, databases, partitions, users, roles, and more.
load
Load a collection or partition.
query
Query entities with filter expressions.
release
Release a collection or partition.
rename
Rename collection.
revoke
Revoke role, privilege, or privilege_group.
search
Perform vector similarity search.
set
Set output format.
show
Show collection, database, partition, index details, and more.
transfer
Transfer replicas between resource groups.
truncate
Remove all data from a collection.
update
Update password or resource group.
upsert
Upsert data into a collection.
use
Use database.
version
Shows the version of Milvus_CLI.