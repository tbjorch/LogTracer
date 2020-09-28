# TraceUtil
Log utility allowing detailed tracing of function execution while at the same time masking arguments by name

## Description
TraceUtil provides a decorator allowing detailed output of function execution to facilitate tracing, while at the same time allowing masking of arguments by argument name. On creation, the provided arguments to TraceUtil will create a list of argument names that will be masked in the log.

## Example implementation:
```
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s  - %(levelname)s - %(message)s')
tu = TraceUtil("password", "pw")
log = logging.getLogger(\_\_name\_\_)

@tu.trace(log)
def login(user, pw, username=None, password=None):
    #function executing stuff

login("Arnold", "MyS3cr3tP4ssw0rd!#", username="pony", password="aqew")
```

The above example produces a log like the below:

```
1970-01-01 12:34:56,789 - __main__ - DEBUG - Executing function login with args=['Arnold', '**********'] and kwargs={'username': 'pony', 'password': '**********'}
```
