from typing import Callable
from logging import Logger
from functools import wraps
import inspect


class LogTracer():
    """
    LogTracer provides a decorator allowing detailed output of function
    execution to facilitate tracing, while at the same time allowing masking
    of arguments by argument name.

    On creation, LogTracer takes a Logger object from the module where it is
    instantiated, and varargs of argument names to be masked.

    Example ----------------------------------------------------------------
    log = logging.getLogger(__name__)
    lt = LogTracer(log, "password", "pw")

    @lt.trace(log)
    def login(user, pw, username=None, password=None):
        # function executing stuff
    ------------------------------------------------------------------------

    The above example produces a log like the below if login is called with
    ("Arnold", "MyS3cr3tP4ssw0rd!#", username="pony", password="aqew") and
    the root logger isformatted like
    '%(asctime)s - %(name)s  - %(levelname)s - %(message)s':

    2020-09-28 19:58:31,733 - my_module_name  - DEBUG - Executing function
    login with args=['Arnold', '**********'] and kwargs={'username': 'pony',
    'password': '**********'}
    """
    def __init__(self, log: Logger, *masked_args: str):
        self.masked_args = masked_args
        self.log = log

    def trace(self) -> Callable:
        def wrapper(function):
            @wraps(function)
            def inner_wrapper(*args, **kwargs):
                arg_obj = inspect.getfullargspec(function)
                self.log.debug(
                    f"Executing function {function.__name__} with "
                    f"{self.__create_arg_log_string(arg_obj, *args, **kwargs)}"
                    f" and {self.__create_kwarg_log_string(**kwargs)}"
                    )
                return function(*args, **kwargs)
            return inner_wrapper
        return wrapper

    def __create_arg_log_string(self, arg_obj, *args, **kwargs) -> str:
        if len(args) == 0:
            return "args=[]"
        arg_list = list(args)
        # Iterating through positional arguments and breaking when/if we
        # reach default arguments, found in the kwarg parameter.
        for i, arg in enumerate(arg_obj.args):
            if i > len(arg_list):
                break
            if arg in self.masked_args:
                arg_list[i] = "**********"
        return f"args={arg_list}"

    def __create_kwarg_log_string(self, **kwargs) -> str:
        for kwarg in kwargs:
            if kwarg in self.masked_args:
                kwargs[kwarg] = "**********"
        return f"kwargs={kwargs}"
