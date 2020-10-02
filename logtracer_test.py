from logtracer import LogTracer
import logging
from io import StringIO
import inspect


class TestContext():
    def __init__(self, *masked_args):
        self.log = logging.getLogger(__name__)
        self.stdout = StringIO()
        sh = logging.StreamHandler(self.stdout)
        self.log.addHandler(sh)
        self.log.setLevel(logging.DEBUG)
        self.lt = LogTracer(self.log, *masked_args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self


def test_posargs_varargs_varkwargs():
    with TestContext("password") as c:
        @c.lt.trace()
        def my_function1(username, password, *args, **kwargs): pass
        my_function1("Arnold", "SuperSecret123!€", "some", "stuff",
                     mykey1="kwarg1", mykey2="kwarg2")
        logstring = c.stdout.getvalue()
        print("masked arguments: ", c.lt.masked_args)
        print("Argspec object: ", inspect.getfullargspec(my_function1))
        assert logstring == \
            "Executing function my_function1 with args=" + \
            "['Arnold', '**********', 'some', 'stuff'] and " + \
            "kwargs={'mykey1': 'kwarg1', 'mykey2': 'kwarg2'}\n"


def test_varags_defaultkwargs_varkwargs():
    with TestContext("password") as c:
        @c.lt.trace()
        def my_function2(*args, username=None, password=None, **kwargs): pass
        my_function2("some", username="Arnold",
                     password="SuperSecret123!€", mykey1="kwarg1")
        logstring = c.stdout.getvalue()
        print("masked arguments: ", c.lt.masked_args)
        print("Argspec object: ", inspect.getfullargspec(my_function2))
        assert logstring == \
            "Executing function my_function2 with args=['some'] and kwargs" + \
            "={'username': 'Arnold', 'password': '**********', 'mykey1': " + \
            "'kwarg1'}\n"


def test_posargs_varargs_defaultkwargs_varkwargs():
    with TestContext("password") as c:
        @c.lt.trace()
        def my_function3(
            usernamearg,
            passwordarg,
            *args,
            username=None,
            password=None,
            **kwargs): pass
        my_function3("Arnold", "SuperSecret123!€", "more", "stuff",
                     username="pony", password="passW0Rd", other="kwarg")
        logstring = c.stdout.getvalue()
        print("masked arguments: ", c.lt.masked_args)
        print("Argspec object: ", inspect.getfullargspec(my_function3))
        assert logstring == \
            "Executing function my_function3 with args=['Arnold', " + \
            "'SuperSecret123!€', 'more', 'stuff'] and kwargs={'username':" + \
            " 'pony', 'password': '**********', 'other': 'kwarg'}\n"


def test_posargs_defaultkwargs():
    with TestContext("pw", "password") as c:
        @c.lt.trace()
        def my_function4(user, pw, username=None, password=None): pass
        my_function4("Arnold", "asdöla231",
                     username="popy", password="asdfgh123456")
        logstring = c.stdout.getvalue()
        print("masked arguments: ", c.lt.masked_args)
        print("Argspec object: ", inspect.getfullargspec(my_function4))
        assert logstring == \
            "Executing function my_function4 with args=" + \
            "['Arnold', '**********'] and kwargs=" + \
            "{'username': 'popy', 'password': '**********'}\n"


def test_posargs():
    with TestContext("pw") as c:
        @c.lt.trace()
        def my_function5(user, pw): pass
        my_function5("Arnold", "asdöla231")
        logstring = c.stdout.getvalue()
        print("masked arguments: ", c.lt.masked_args)
        print("Argspec object: ", inspect.getfullargspec(my_function5))
        assert logstring == \
            "Executing function my_function5 with args=" + \
            "['Arnold', '**********'] and kwargs={}\n"


def test_defaultkwargs_1():
    with TestContext("password") as c:
        @c.lt.trace()
        def my_function6(username=None, password=None): pass
        my_function6("Arnold", "asdöla231")
        logstring = c.stdout.getvalue()
        print("masked arguments: ", c.lt.masked_args)
        print("Argspec object: ", inspect.getfullargspec(my_function6))
        assert logstring == \
            "Executing function my_function6 with " + \
            "args=['Arnold', '**********'] and kwargs={}\n"


def test_defaultkwargs_2():
    with TestContext("password") as c:
        @c.lt.trace()
        def my_function6(username=None, password=None): pass
        my_function6(password="asdöla231", username="Bernard")
        logstring = c.stdout.getvalue()
        print("masked arguments: ", c.lt.masked_args)
        print("Argspec object: ", inspect.getfullargspec(my_function6))
        assert logstring == \
            "Executing function my_function6 with args=[] " + \
            "and kwargs={'password': '**********', 'username': 'Bernard'}\n"


def test_defaultkwargs_3():
    with TestContext("password") as c:
        @c.lt.trace()
        def my_function6(username=None, password=None): pass
        my_function6(username="Arnold", password="asdöla231")
        logstring = c.stdout.getvalue()
        print("masked arguments: ", c.lt.masked_args)
        print("Argspec object: ", inspect.getfullargspec(my_function6))
        assert logstring == \
            "Executing function my_function6 with args=[] " + \
            "and kwargs={'username': 'Arnold', 'password': '**********'}\n"


def test_varargs_defaultkwargs_varkwargs():
    with TestContext("password") as c:
        @c.lt.trace()
        def my_function7(*args, password=None, **kwargs): pass
        my_function7("Arnold", "asdöla231", password="asdfgh123456",
                     some="stuff", going="here")
        logstring = c.stdout.getvalue()
        print("masked arguments: ", c.lt.masked_args)
        print("Argspec object: ", inspect.getfullargspec(my_function7))
        assert logstring == \
            "Executing function my_function7 with args=['Arnold', " + \
            "'asdöla231'] and kwargs={'password': '**********', " + \
            "'some': 'stuff', 'going': 'here'}\n"
