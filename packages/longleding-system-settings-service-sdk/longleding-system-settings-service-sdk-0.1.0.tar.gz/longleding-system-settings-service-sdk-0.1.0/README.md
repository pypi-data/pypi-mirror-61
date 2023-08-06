Longleding System Settings Service SDK

# Supported Python Versions

Python >= 3.6

# Installation

longleding-system-settings-service-sdk is available for Linux, macOS, and Windows.

```shell script
$ pip install longleding-system-settings-service-sdk
```

# Basic Usage

```python

```

# Troubleshoot

If you encounter error messages similar to the following:

```shell script
...
TypeError: Couldn't build proto file into descriptor pool!
Invalid proto descriptor for file "common.proto":
  common.proto: A file with this name is already in the pool.
```

Setting an environment variable the following before running:

```shell script
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION='python'
```

See also
- [[Python] A file with this name is already in the pool.](#https://github.com/protocolbuffers/protobuf/issues/3002)
- [Python Generated Code](#https://developers.google.com/protocol-buffers/docs/reference/python-generated)