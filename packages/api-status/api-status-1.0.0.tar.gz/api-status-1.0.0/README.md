# Status
[![PEP8](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![coverage report](https://gitlab.com/cdlr75/status/badges/master/coverage.svg)](https://gitlab.com/cdlr75/status/-/commits/master)


Simple way to make a /status for your services with python and asyncio.

## Install

```sh
pip install api-status
```

## How it works ?

**TL;DR;**

Check a working example at:
https://gitlab.com/cdlr75/status/-/blob/develop/tests/learning/example.py


Let say you have a coroutine that replies a dict with the desired status of your service.
```py
async def status():
    """ Returns our service status.

    :returns: Misc info about our service.
    :rtype: dict
    """
    return {
        "name": "MyService",
        "status": "ok",
        "version": "v1"
    }
```
With `status`, to expose this throught an HTTP endpoint:
```py
from status import Server

server = Server(host="127.0.0.1", port=8080)
# register our status endpoint
server.add_route(status, method="GET", path=r"/status")
await server.start()
# the status is now available at http://127.0.0.1:8080/status
```
If you take care of gracefull shutdowns for your services, call the method `stop`:
```py
await server.stop()
```
