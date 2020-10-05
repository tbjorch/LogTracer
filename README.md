# LogTracer
Log utility allowing detailed tracing of function execution while at the same time masking arguments by name

## Description
LogTracer provides a decorator method, enabling detailed output of function execution to facilitate tracing, while at the same time allowing masking of arguments by argument name. The trace method will mask the value of arguments with a name matching any of the string arguments provided to the method.

## Example implementation:
```Python
import logging
from logtracer import LogTracer

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s  - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
lt = LogTracer(log)

@lt.trace("password", "pw")
def login(user, pw, username=None, password=None):
    pass

login("Arnold", "MyS3cr3tP4ssw0rd!#", username="pony", password="aqew")
```

The above example produces a log like the below:

```
1970-01-01 12:34:56,789 - __main__ - DEBUG - Executing function login with args=['Arnold', '**********'] and kwargs={'username': 'pony', 'password': '**********'}
```
