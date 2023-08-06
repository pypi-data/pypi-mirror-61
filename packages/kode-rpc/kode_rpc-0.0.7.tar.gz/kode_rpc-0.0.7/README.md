# kode_rpc

### Server Usage
```python
from typing import Mapping
import asyncio
import logging

from kode_rpc.method import RPCMethod, method
from kode_rpc.server import RPCServer, RPCRequestInfo


@method(version=1)
async def some_rpc_method(param: str):
    return {'result': True}


async def rpc_logger(rpc_method: RPCMethod, result: Mapping, request_info: RPCRequestInfo):
    logging.info('rpc_log', extra={
        'rpc_name': rpc_method.name,
        'rpc_result': result,
        'trace_id': request_info.trace_id,
        'master': request_info.master
    })


async def rpc_exception_handler(rpc_method: RPCMethod, exc: BaseException, request_info: RPCRequestInfo) -> Mapping:
    if isinstance(exc, RuntimeError):
        return {
            'error': {
                'code': 'RuntimeError',
                'trace_id': request_info.trace_id
            }
        }
    else:
        return {
            'error': {
                'code': 'ServerError',
                'trace_id': request_info.trace_id
            }
        }


async def main():
    logging.basicConfig(level=logging.INFO)

    server = RPCServer('my_service', rabbitmq_host='localhost', rabbitmq_user='guest', rabbitmq_password='guest')
    server.method_logger(rpc_logger)
    server.method_exception_handler(rpc_exception_handler)

    await server.register_methods([some_rpc_method])
    await server.serve()


if __name__ == '__main__':
    asyncio.run(main())
```

### Client Usage
```python
import asyncio

from kode_rpc.client import RPCClient

# To access rpc_client from anywhere it must be initialized at top level module
rpc_client = RPCClient('client_name')


async def main():
    # Connect to rpc broker once at startup
    await rpc_client.connect(rabbitmq_host='localhost', rabbitmq_user='guest', rabbitmq_password='guest')

    # ...
    # Somewhere in logic
    result = await rpc_client.call(
        service_name='my_service', 
        method='rpc_method', 
        payload={'param': 'any'}
    )
    # => {'result': True}
    
    # When application is shutting down do not forget to disconnect from rpc broker
    await rpc_client.disconnect()


if __name__ == '__main__':
    asyncio.run(main())
```
