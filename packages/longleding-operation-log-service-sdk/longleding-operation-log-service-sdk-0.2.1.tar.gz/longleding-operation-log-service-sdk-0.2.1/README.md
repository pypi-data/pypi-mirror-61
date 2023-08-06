Longleding Operation Log Service SDK

# Supported Python Versions

Python >= 3.6

# Installation

longleding-operation-log-service-sdk is available for Linux, macOS, and Windows.

```shell script
$ pip install longleding-operation-log-service-sdk
```

# Basic Usage

```python
# -*- coding: utf-8 -*-
from datetime import datetime
import operation_log_service_sdk

operation_log_service_endpoint = "localhost:80"
source_name = "demo"

operation_log_service_sdk.init_service(endpoint=operation_log_service_endpoint, source=source_name)


def put_log():
    log = {
        "time": datetime.now(),
        "topic": "tpc",
        "tags": {"tg1": "v1", "tg2": "v2"},
        "content": "say something."
    }
    operation_log_service_sdk.log(**log)


def get_logs():
    end_time = datetime.now()
    start_time = datetime.strptime(("%d-%02d-%02d 00:00:00" % (end_time.year, end_time.month, end_time.day)), "%Y-%m-%d %H:%M:%S")
    request = {
        "start_time": start_time,
        "end_time": end_time,
        "offset": 0,
        "limit": 0,
        "reverse": False,
        "topic_in": ["tpc", "other"],
        "source_in": ["demo", "other"],
        "tag_contains": {
            "tg1": ["v1", "v8"],
            "tg2": [],
        },
    }
    print("request: " + str(request))
    print("\n================================\n")
    resp = operation_log_service_sdk.get_operation_logs(**request)
    for v in resp:
        print(v)


if __name__ == '__main__':
    put_log()
    get_logs()

```
