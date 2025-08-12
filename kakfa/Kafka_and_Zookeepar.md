
Basic (to test fundamentals)

Intermediate (real-world scenarios)

Advanced (deep Kafka/Zookeeper internals)

Kafka Questions
What is Apache Kafka and why is it used?

Explain the difference between Kafka topics, partitions, and offsets.

What is the difference between Kafka producer and consumer?

What is a consumer group in Kafka and how does it work?

Explain message ordering in Kafka.

How does Kafka achieve high throughput and fault tolerance?

Difference between Kafka replication factor and partition count.

What is Kafka log retention policy and how do you configure it?

How is exactly-once delivery achieved in Kafka?

What happens if a Kafka broker fails?

What’s the difference between a leader and follower replica in Kafka?

How do you handle backpressure in Kafka consumers?

What are Kafka Streams and when would you use them?

Explain ISR (In-Sync Replica) in Kafka.

How does Kafka ensure durability of messages?

Zookeeper Questions
What is Zookeeper and why is it used in Kafka?

Explain the role of Zookeeper in Kafka cluster coordination.

What is a Znode in Zookeeper?

Difference between persistent and ephemeral znodes.

What is the role of the Zookeeper leader?

How does Zookeeper handle leader election in Kafka?

What happens if Zookeeper goes down in a Kafka cluster?

How does Zookeeper store its data?

Explain Zookeeper watches and notifications.

Why is Zookeeper being removed in newer Kafka versions?

Scenario-based Questions
If you have 3 brokers, replication factor = 3, and one broker goes down, what happens to your data?

If your Kafka topic has 1 partition but 3 consumers in a group, how will messages be distributed?

How would you migrate from a Zookeeper-based Kafka cluster to KRaft mode (without Zookeeper)?

You have a consumer lag issue — how do you troubleshoot it?

If the producer sends data faster than consumers can process, what are your options?
















Kafka Questions & Answers
1. What is Apache Kafka and why is it used?

Apache Kafka is a distributed streaming platform.

Used for real-time data pipelines and stream processing.

Handles high-throughput, low-latency messaging between systems.

2. Difference between Kafka topics, partitions, and offsets:

Topic → Logical channel for messages.

Partition → Splits a topic into multiple logs for scalability.

Offset → Position of a message in a partition.

3. Difference between Kafka producer and consumer:

Producer → Publishes messages to a topic.

Consumer → Reads messages from a topic.

4. What is a consumer group in Kafka?

Group of consumers that share the work of consuming from a topic.

Each partition is consumed by only one consumer in the group.

5. Explain message ordering in Kafka:

Ordering is guaranteed per partition, not across all partitions.

6. How does Kafka achieve high throughput and fault tolerance?

Sequential disk writes + page cache.

Partitioned topics for parallelism.

Replication for fault tolerance.

7. Difference between replication factor and partition count:

Replication factor → Number of copies of a partition.

Partition count → Number of segments a topic is split into.

8. Kafka log retention policy:

Controls how long data is kept.

Can be set by time (log.retention.hours) or size (log.retention.bytes).

9. Exactly-once delivery in Kafka:

Achieved using idempotent producers and transactions.

10. What happens if a Kafka broker fails?

Leader election happens among replicas.

Consumers continue reading from new leaders.

11. Difference between leader and follower replica:

Leader → Handles reads/writes.

Follower → Syncs data from leader.

12. How to handle backpressure in consumers:

Tune fetch.min.bytes, max.poll.records.

Add more consumers.

Use batch processing.

13. What are Kafka Streams?

Kafka’s library for real-time processing of messages.

14. What is ISR (In-Sync Replica)?

Replicas that have the latest committed data from the leader.

15. How does Kafka ensure durability of messages?

Writes to disk before acknowledging to producer.

Replication across brokers.

Zookeeper Questions & Answers
1. What is Zookeeper and why is it used in Kafka?

Distributed coordination service.

Manages broker metadata, topic configs, and leader election.

2. Role of Zookeeper in Kafka cluster coordination:

Tracks broker membership.

Stores topic configurations.

Manages leader election for partitions.

3. What is a Znode in Zookeeper?

A data node in Zookeeper’s tree structure.

4. Difference between persistent and ephemeral znodes:

Persistent → Stays until explicitly deleted.

Ephemeral → Exists only while session is active.

5. Role of Zookeeper leader:

Handles write requests and syncs with followers.

6. How does Zookeeper handle leader election in Kafka?

Uses ephemeral znodes to determine the active controller broker.

7. What happens if Zookeeper goes down?

Kafka can still serve reads/writes temporarily,
but new leaders cannot be elected and no metadata changes can occur.

8. How does Zookeeper store its data?

Stores in-memory with snapshots + transaction logs on disk.

9. Zookeeper watches and notifications:

Clients can set watches on znodes to get notified of changes.

10. Why is Zookeeper being removed in newer Kafka versions?

Kafka KRaft mode replaces it with an internal quorum controller.

Reduces complexity and external dependency.

Scenario-based Q&A
1. If you have 3 brokers, replication factor = 3, and one broker goes down:

Data is still available from remaining brokers.

Once the broker comes back, it syncs data.

2. Topic with 1 partition but 3 consumers in a group:

Only one consumer gets the messages. Others stay idle.

3. Migrating from Zookeeper-based Kafka to KRaft mode:

Create a new KRaft cluster.

Use MirrorMaker 2 or topic export/import for migration.

4. Troubleshooting consumer lag:

Check broker health, network latency, slow consumers, or small fetch sizes.

5. Producer sends data faster than consumers can process:

Add consumers, increase partitions, enable batching, or throttle producer.








Yes ✅ — this topics → partitions → offsets concept is exactly what makes Kafka work efficiently when your code runs on multiple machines.

Here’s why:

1. Topic → Logical Channel
If your app runs on multiple machines, all producers can send data to the same topic name.

All consumers can read from that topic without stepping on each other’s toes.

2. Partition → Scalability Across Machines
Kafka splits a topic into partitions.

Each partition can be stored on different brokers (Kafka servers) and processed by different consumer instances.

This means multiple machines can process different parts of the data in parallel.

Example:

Topic: Orders

Partitions: 3

Consumers: 3 instances of your app
→ Each instance reads from one partition, so the load is balanced.

3. Offset → Tracking Where You Left Off
Every message in a partition has a unique offset (like a line number).

Even if multiple machines are consuming from the same topic, Kafka tracks offsets per consumer group.

This ensures each machine knows exactly where to resume if it restarts or crashes.

💡 In short:

Partitions let Kafka spread the work across machines for speed and scalability.

Offsets let each machine reliably pick up where it left off.

This is why Kafka is perfect for distributed systems.

If you want, I can draw you a machine-to-partition mapping diagram to make this visually clear. That’s a common interview question follow-up.









Ask ChatGPT





<!-- ------------------------------------------------------------------------------------------ -->
1. Kafka Producer
What it does: Sends (publishes) messages to a Kafka topic.

Think of it as a writer.

It doesn’t care who will read the messages — it just puts them into Kafka.

Example:

An e-commerce app’s order service produces messages like "OrderID=1234, Status=PLACED" into a topic called "orders".

2. Kafka Consumer
What it does: Reads (subscribes to) messages from a Kafka topic.

Think of it as a reader.

It processes the messages and can act upon them (store in DB, trigger workflows, etc.).

Example:

A shipping service consumes from "orders" topic and sees "OrderID=1234, Status=PLACED", then starts shipping.

📌 Key Difference:

Producer = "I send data into Kafka."

Consumer = "I read data from Kafka."

If you want, I can also give you a real-world analogy so you’ll never forget this.
Want me to do that?



<!-- 3. Difference between Kafka producer and consumer: -->
1. Kafka Producer
What it does: Sends (publishes) messages to a Kafka topic.

Think of it as a writer.

It doesn’t care who will read the messages — it just puts them into Kafka.

Example:

An e-commerce app’s order service produces messages like "OrderID=1234, Status=PLACED" into a topic called "orders".

2. Kafka Consumer
What it does: Reads (subscribes to) messages from a Kafka topic.

Think of it as a reader.

It processes the messages and can act upon them (store in DB, trigger workflows, etc.).

Example:

A shipping service consumes from "orders" topic and sees "OrderID=1234, Status=PLACED", then starts shipping.

📌 Key Difference:

Producer = "I send data into Kafka."

Consumer = "I read data from Kafka."

<!-- 4. Difference between persistent and ephemeral znodes:  -->


Persistent → Stays until explicitly deleted.

Ephemeral → Exists only while session is active.



1. Persistent Znode
Lifespan: Stays in Zookeeper until explicitly deleted by a client.

Use case: Store configuration, metadata, or any data that must survive client disconnections.

Example:

You create /config/db_host = "192.168.1.10" — even if your client disconnects, it stays until you delete it.

2. Ephemeral Znode
Lifespan: Exists only while the session that created it is active.

Once the client disconnects or session expires, the znode is automatically deleted.

Use case: Track temporary states, like service availability in leader election or service discovery.

Example:

A service registers itself at /services/worker1 as an ephemeral node. If the service crashes, the node disappears — others know it’s gone.

📌 Key Difference:

Persistent = Manual deletion required.

Ephemeral = Auto-deletes on session end.

<!-- 5. Role of Zookeeper leader: -->


Handles write requests and syncs with followers.


Role of Zookeeper Leader
Primary responsibility:

Processes all write requests from clients.

Coordinates updates so data stays consistent across all nodes.

How it works:

When a write request comes, the Leader validates and assigns a transaction ID.

It sends the change to Followers for replication.

Waits for a majority (quorum) of followers to acknowledge.

Once quorum is reached, commits the change and notifies followers.

Extra role:

Maintains synchronization between nodes.

Handles ephemeral node removal when sessions expire.

📌 In short:
Leader in Zookeeper = Traffic cop for writes + Sync master for data consistency.

<!-- 6. How does Zookeeper handle leader election in Kafka?  -->


Uses ephemeral znodes to determine the active controller broker.

6. How Zookeeper handles leader election in Kafka
Trigger for election

Leader election happens when:

The current broker acting as controller (Kafka’s leader broker) fails or disconnects.

A new broker joins and triggers rebalancing.

Zookeeper’s role

Kafka stores the controller information in a special ZNode (e.g., /controller).

This node is ephemeral, meaning it exists only while the leader broker session is active.

If the session ends, Zookeeper automatically deletes it → this signals to other brokers that a new election is needed.

Election process

All available brokers try to create the /controller ZNode at the same time.

Zookeeper allows only one broker to succeed (first-come-first-serve).

The broker that succeeds becomes the new controller (leader).

Post-election

The new controller assigns partitions and leaders to other brokers.

Ensures all followers are aware of the new leader and replication resumes.

📌 In short:
Zookeeper uses ephemeral znodes + first-come creation to decide who the Kafka leader is when the current leader fails.



<!-- 7. What happens if Zookeeper goes down? -->



Kafka can still serve reads/writes temporarily,
but new leaders cannot be elected and no metadata changes can occur.

7. What happens if Zookeeper goes down?
Existing operations continue (for a while)

Kafka brokers already know their partition assignments and leaders from the last successful Zookeeper connection.

Producers can still send messages to the current partition leaders.

Consumers can still fetch data from the brokers.

Limitations while Zookeeper is down

No new leader election → If a leader broker fails, there’s no way to choose a replacement.

No metadata updates → Cannot create topics, delete topics, or change configurations.

No rebalance → New brokers joining won’t be assigned partitions.

Impact grows over time

If no broker fails → Kafka continues working as normal (read/write works).

If a broker or partition leader fails → That partition becomes unavailable because no election can be held.

When Zookeeper comes back

Brokers reconnect and resume normal cluster operations.

Pending leader elections or metadata changes get processed.

💡 In short:
Zookeeper going down is like the cluster’s brain going offline — the body (Kafka brokers) can keep moving for a while, but if something goes wrong, it can’t make new decisions.

<!-- 8. How does Zookeeper store its data?  -->



Stores in-memory with snapshots + transaction logs on disk.
8. How does Zookeeper store its data?
In-memory data tree

Zookeeper keeps the entire hierarchical data structure (znodes and their data) in memory for fast reads.

This is why reads are super quick.

Snapshots on disk

Periodically, Zookeeper writes a snapshot of its entire in-memory data tree to disk.

This snapshot is a full dump of the current state, allowing quick recovery after restart.

Transaction logs (write-ahead logs)

Every change (create, update, delete) is recorded in an append-only transaction log on disk.

This ensures durability — if Zookeeper crashes, it can replay logs after loading the latest snapshot to recover recent changes.

Recovery process

On startup, Zookeeper loads the latest snapshot from disk into memory.

Then replays transaction logs that occurred after the snapshot to bring data up to date.

📌 In short:
Zookeeper uses in-memory data for speed, combined with snapshots and transaction logs on disk for durability and recovery.



<!-- 9. Zookeeper watches and notifications:  -->



Clients can set watches on znodes to get notified of changes.


9. Zookeeper Watches and Notifications
What is a watch?

A watch is a one-time trigger that clients can set on a specific znode (data node).

It lets the client get notified when something changes on that znode — such as data change, deletion, or creation of children.

How watches work:

When a client sets a watch on a znode, Zookeeper stores this watch for that client session.

As soon as the watched event occurs (e.g., the znode’s data changes), Zookeeper sends a notification event to the client.

The watch is then removed (one-time trigger). If the client wants continuous notifications, it must reset the watch.

Types of watches:

Data watches: Triggered when the data of a znode changes.

Existence watches: Triggered when a znode is created or deleted.

Child watches: Triggered when the children of a znode change (added or removed).

Use cases:

Service discovery — clients watch for availability of services.

Configuration changes — apps watch config nodes to reload settings dynamically.

Leader election — participants watch leader node changes to trigger re-election.

📌 In short:
Watches provide a push-style notification mechanism so clients don’t have to poll Zookeeper continuously, enabling efficient and reactive distributed coordination.

<!-- 10. Why is Zookeeper being removed in newer Kafka versions? -->

10. Why is Zookeeper being removed in newer Kafka versions?

Kafka KRaft mode replaces it with an internal quorum controller.

Reduces complexity and external dependency.

Scenario-based Q&A
1. If you have 3 brokers, replication factor = 3, and one broker goes down:

Data is still available from remaining brokers.

Once the broker comes back, it syncs data.

2. Topic with 1 partition but 3 consumers in a group:

Only one consumer gets the messages. Others stay idle.

3. Migrating from Zookeeper-based Kafka to KRaft mode:

Create a new KRaft cluster.

Use MirrorMaker 2 or topic export/import for migration.

4. Troubleshooting consumer lag:

Check broker health, network latency, slow consumers, or small fetch sizes.

5. Producer sends data faster than consumers can process:

Add consumers, increase partitions, enable batching, or throttle producer.





10. Why is Zookeeper being removed in newer Kafka versions?
Kafka’s new KRaft mode (Kafka Raft Metadata mode) replaces Zookeeper with an internal quorum controller.

This means Kafka manages metadata (brokers, topics, partitions, ACLs) internally using a Raft consensus algorithm.

Benefits:

Reduces operational complexity (no separate Zookeeper cluster to maintain).

Improves scalability and reliability of metadata management.

Simplifies Kafka architecture.

Scenario-based Q&A
1. If you have 3 brokers, replication factor = 3, and one broker goes down:

The other two brokers keep serving data (no data loss).

When the downed broker comes back, it syncs missing data to catch up.

2. Topic with 1 partition but 3 consumers in a group:

Only one consumer will read all messages from that single partition.

Other two consumers will remain idle since Kafka assigns each partition to only one consumer in the group.

3. Migrating from Zookeeper-based Kafka to KRaft mode:

Set up a new Kafka cluster in KRaft mode without Zookeeper.

Use tools like MirrorMaker 2 to replicate topics and data from old cluster to new.

Alternatively, export/import topics and configurations manually.

4. Troubleshooting consumer lag:

Check if brokers are healthy and available.

Monitor network latency or bandwidth issues.

Make sure consumers are not slow or stuck.

Adjust consumer configurations like fetch.min.bytes and max.poll.records.

5. Producer sends data faster than consumers can process:

Add more consumers in the consumer group (horizontal scaling).

Increase the number of partitions for parallel processing.

Enable batching in producer and consumer for efficiency.

Use backpressure mechanisms or throttle producer speed.