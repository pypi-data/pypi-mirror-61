# SwarmLib Repository

This library facillitates access to the Swarm network.


# Examples

The SwarmLib makes it easy to create Swarm Agents. There are two types of Agents: Consumers and Providers. See the examples below.

## Consumer
A consumer is an agent that only uses the Swarm resources. For example:

```python
from swarm_lib import Consumer
consumer = Consumer(keys_file="keys.json")
query = {
    "operation": {"@type": "swarm:ReadOperation", "returns": "swarm:Image"},
    "usageDuration": 30
}
image_executor = consumer.get_executor(query)
if image_executor.contract_providers():
    result = image_executor.execute()
```

## Provider
A provider makes resources available to the Swarm. For example:

```python
from flask import Flask, request, jsonify
from swarm_lib import Provider
from onboard_camera import read_frame

app = Flask(__name__)

provider = Provider(
    description_file="./description.jsonld",
    policies_file="./policies.json",
    keys_file="./keys.json"
)

@app.route("/camera-service/image", methods=['GET'])
@provider.enforce_authorization
def get_frame():
    try:
        return jsonify(read_frame())
    except Exception as e:
        return jsonify({"error": "could not get frame from onboard camera"})

if __name__ == "__main__":
    if provider.join_swarm():
        app.run(host="0.0.0.0", port=provider.port(), threaded=True, debug=True, use_reloader=True)
    else:
        print("Could not join the Swarm Network")
```


# Usage

Install with pip:

```bash
pip3 install swarm_lib
```

Follow the examples above to build your own Swarm Agents.


# Contributing

## Dependencies

```bash
sudo apt install python3-pip python3-setuptools python3-dev
pip3 install -r requirements.txt
```

## Publish a new version

To make a new release, follow these steps:

1. Update the version in `setup.py`
2. Run `python3 setup.py sdist bdist_wheel` to create a distributable release
3. Run `python3 -m twine upload dist/*` to upload to pip

If a password is asked and you don't know what to do, ask the maintainer (Geovane Fedrecheski).
