from typing import Callable
from logging import Logger
from functools import wraps
import inspect


class TraceUtil():
    """
    TraceUtil provides a decorator allowing detailed output of function
    execution to facilitate tracing, while at the same time allowing masking
    of arguments by argument name.

    On creation, TraceUtil takes varargs of argument names to be masked

    Example ----------------------------------------------------------------
    tu = TraceUtil("password", "pw")
    log = logging.getLogger(__name__)

    @tu.trace(log)
    def login(user, pw, username=None, password=None):
        # function executing stuff
    ------------------------------------------------------------------------

    The above example produces a log like the below if login is called with
    ("Arnold", "MyS3cr3tP4ssw0rd!#", username="pony", password="aqew") and
    the root logger isformatted like
    '%(asctime)s - %(name)s  - %(levelname)s - %(message)s':

    2020-09-28 19:58:31,733 - my_module_name  - DEBUG - Executing function login with args=['Arnold', '**********'] and kwargs={'username': 'pony', 'password': '**********'}
    """
    def __init__(self, *excluded_args: str):
        self.excluded_args = excluded_args

    def trace(self, log: Logger) -> Callable:
        """
        Decorator method creating trace log.

        Parameters:
        log - Logger object in order to ensure outputed log conforms to
              the formatting configured in root

        Returns:
        Decorated function
        """
        def wrapper(function):
            @wraps(function)
            def inner_wrapper(*args, **kwargs):
                arg_obj = inspect.getfullargspec(function)
                log.debug(
                    f"Executing function {function.__name__} with "
                    f"{self.__create_arg_log_string(arg_obj, *args, **kwargs)}"
                    f" and {self.__create_kwarg_log_string(arg_obj, **kwargs)}"
                    )
                return function(*args, **kwargs)
            return inner_wrapper
        return wrapper

    def __create_arg_log_string(self, arg_obj, *args, **kwargs) -> str:
        if arg_obj.defaults is not None \
                and len(arg_obj.args) == len(arg_obj.defaults) \
                and len(args) == 0:
            return "args=[]"
        arg_list = list(args)
        for i, arg in enumerate(arg_obj.args):
            if (arg_obj.defaults is not None) \
                    and (i > len(arg_obj.defaults)-1):
                break
            if arg in self.excluded_args:
                arg_list[i] = "**********"
        return f"args={arg_list}"

    def __create_kwarg_log_string(self, arg_obj, **kwargs) -> str:
        if (arg_obj.defaults is not None) \
                and (len(kwargs) == len(arg_obj.defaults)):
            for arg in arg_obj.args:
                if arg in self.excluded_args:
                    kwargs[arg] = "**********"
            return f"kwargs={kwargs}"
        for kwarg in arg_obj.kwonlyargs:
            if kwarg in self.excluded_args:
                kwargs[kwarg] = "**********"
        return f"kwargs={kwargs}"
