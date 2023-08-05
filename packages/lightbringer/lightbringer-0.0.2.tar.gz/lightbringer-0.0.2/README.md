# lightbringer

Very simple NSQ client library. Exposes a very small API to publish and read from a NSQ cluster.

Supports only (but supports them well, with a complete test suite covering all the code)
- TCP connections to nsqd (no HTTP connections)
- nsqlookupd setups
- publish only to a single server
- keepalives (TOUCH) of inflight messages
- messages are requeued at connection close

Not supported:
- tls connections
- snappy/deflate connections


### Examples

#### Write

```python
mesage = b'some data'
async with lightbringer.Writer('127.0.0.1:4150', topic='topic') as writer:
	await writer.pub(message)
	await writer.dpub(message, delay)
```

#### Read from `nsqd` servers
```python
async with lightbringer.Reader(
	nsqd_tcp_addresses=['127.0.0.1:4150'],
	lookupd_http_addresses=['http://127.0.0.1:4161'], # will poll this regularly and merge with the list of direct connections
	topic='topic',
	channel='channel#ephemeral',
) as reader:
	async for msg in reader:
		print(msg, msg.nsqd_host, msg.body)
		await msg.touch()
		await msg.fin()
		await msg.req()
		await msg.req(timeout=10)
```
