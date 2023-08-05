# Adsocket transport

## Install

``` bash
pip install adsocket-transport
```

## Usage

Transport initialization and sending message is very simple

```python
from adsocket_transport import ADSocketTransport

adsocket = ADSocketTransport(
        driver='redis',
        host='redis://localhost:6379',
        db=1
    )

adsocket.send_data(data={'obj': 'user', 'obj_id': 4}, channels={'name': 'global', 'id': 'global'})
```

in case of async transport

```python
from adsocket_transport import ADSocketAsyncTransport

adsocket = ADSocketAsyncTransport(
        driver='redis',
        host='redis://localhost:6379',
        db=1
    )
await adsocket.send_data(data={'obj': 'user', 'obj_id': 4}, channels={'name': 'global', 'id': 'global'})
```

Alternatively you can create message manually
```python
from adsocket_transport import Message, ADSocketAsyncTransport

adsocket = ADSocketAsyncTransport(
        driver='redis',
        host='redis://localhost:6379',
        db=1
    )

message = Message(type='publish', data={'obj': 'user', 'obj_id': 4}, channel='global', channel_id='global')
await adsocket.send(message)
```

For more see [adsocket-transport](https://github.com/AwesomeDevelopersUG/adsocket).
