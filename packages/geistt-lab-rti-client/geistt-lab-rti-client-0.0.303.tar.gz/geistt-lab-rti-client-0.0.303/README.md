# GEISTT Lab RTI Client for Python

Example usage:

```python
from geistt_lab_rti_client import RTI, proto, constants

rti = RTI(application_id="python_test")

def on_connect():
    print("Connected")
rti.on("connect", on_connect)

def on_error(channel, message, exception):
    print(f"Error: {channel}: {message}", file=sys.stderr)
rti.on("error", on_error)

def on_message(content): print(f"received: {content}")
self.rti.subscribe_text("test", on_message)
self.rti.publish_text("test", "foo")
```