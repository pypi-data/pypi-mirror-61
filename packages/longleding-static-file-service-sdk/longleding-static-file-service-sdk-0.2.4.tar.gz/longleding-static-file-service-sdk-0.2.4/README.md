Longleding Static File Service SDK

# Supported Python Versions

Python >= 3.6

# Installation

longleding-static-file-service-sdk is available for Linux, macOS, and Windows.

```shell script
$ pip install longleding-static-file-service-sdk
```

# Basic Usage

```python
# -*- coding: utf-8 -*-
import static_file_service

static_file_service_endpoint = "localhost:80"
static_file_service.init_service(endpoint=static_file_service_endpoint)


if __name__ == '__main__':
    test_bytes = b'test file'
    print(static_file_service.get_oss_bucket_info())
    print(static_file_service.get_upload_credentials())
    static_file_service.put_file('upload/t.txt', test_bytes)
    print(static_file_service.get_file('upload/t.txt'))
    print(static_file_service.get_file_md5('upload/t.txt'))
    static_file_service.copy_file('upload/t.txt', 'upload/t1.txt')
    print(static_file_service.get_file_md5('upload/t1.txt'))
    static_file_service.move_file('upload/t.txt', 'upload/t2.txt')
    print(static_file_service.get_file_md5('upload/t2.txt'))

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