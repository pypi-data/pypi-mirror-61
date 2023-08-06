====
andi
====

.. image:: https://img.shields.io/pypi/v/andi.svg
   :target: https://pypi.python.org/pypi/andi
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/andi.svg
   :target: https://pypi.python.org/pypi/andi
   :alt: Supported Python Versions

.. image:: https://travis-ci.com/scrapinghub/andi.svg?branch=master
   :target: https://travis-ci.com/scrapinghub/andi
   :alt: Build Status

.. image:: https://codecov.io/github/scrapinghub/andi/coverage.svg?branch=master
   :target: https://codecov.io/gh/scrapinghub/andi
   :alt: Coverage report

.. warning::
    Current status is "experimental".

``andi`` tells which kwargs should to be passed to a callable, based
on callable arguments' type annotations.

``andi`` is useful as a building block for frameworks, or as a library
which helps to implement dependency injection (thus the name -
ANnotation-based Dependency Injection).

License is BSD 3-clause.

Installation
============

::

    pip install andi

andi requires Python >= 3.5.3.

Idea
====

``andi`` does a simple thing, but it requires some explanation why
this thing is useful.

You're building a framework. This framework has code which calls some
user-defined function (callback). Callback receives arguments
``foo`` and ``bar``:

.. code-block:: python

    def my_framework(callback):
        # ... compute foo and bar somehow
        result = callback(foo=foo, bar=bar)
        # ...

Then you decide that you want the framework to be flexible,
and support callbacks which take

* both ``foo`` and ``bar``,
* only ``foo``,
* only ``bar``,
* nothing.

If a callback only takes ``foo``, it may be unnecessary to compute ``bar``.

In addition to that, you realize that there can be environments
or implementations where ``foo`` is available for the framework,
but ``bar`` isn't, but you still want to reuse the callbacks which
work without ``bar``, and disable (or error) those who need ``bar``.

So, the logic is the following:

1. Framework defines which inputs are available, or can be possibly computed
   (e.g. ``foo`` and ``bar``).
2. Callback declares which inputs it receives (e.g. ``bar``).
3. Framework inspects the callback, finds arguments the callback needs.
4. Optional: if there are some arguments which callback needs,
   but framework doesn't provide, an error is raised (or callback is disabled).
5. Framework computes argument values (``bar`` in this case).
6. Framework calls the callback.

Depending on implementation, steps 1-5 may happen iteratevely - e.g.
middlewares may be populating different parts of callback kwargs.
In this case step (4 - raising an error) can be skipped.

``andi`` is a library which helps to support this workflow.

Usage
=====

``andi`` usage looks like this:

.. code-block:: python

    import andi

    class Foo:
        pass

    class Bar:
        pass

    class Baz:
        pass


    # use type annotations to declare which inputs a callback wants
    def my_callback1(foo: Foo):
        pass


    def my_callback2(bar: Bar, foo: Foo):
        pass


    def my_framework(callback):
        kwargs_to_provide = andi.to_provide(callback,
                                            can_provide={Foo, Bar, None})
        # for my_callback: kwargs_to_provide == {'foo': Foo}

        # Create all the dependencies - implementation is framework-specific,
        # and can be organized in different ways. Code below is an example.
        kwargs = {}
        for name, cls in kwargs_to_provide.items():
            if cls is Foo:
                kwargs[name] = Foo()
            elif cls is Bar:
                kwargs[name] = fetch_bar()
            elif cls is None:
                kwargs[name] = None
            else:
                raise Exception("Unexpected type")  # shouldn't really happen

        # everything is ready, call the callback
        result = callback(**kwargs)
        # ...

    my_framework(my_callback1)  # Foo instance is passed to my_callback1
    my_framework(my_callback2)  # Bar and Foo instances are passed to my_callback2


If a callback wants some input which framework can't provide,
then some arguments are going to be  missing in kwargs,
and Python can raise TypeError, as usual.
It is possible to check it explicitly, to avoid doing unnecessary
work creating values for other arguments:

.. code-block:: python

    arguments = andi.inspect(callable)
    kwargs_to_provide = andi.to_provide(arguments,
                                        can_provide={Foo, Bar, None})
    cant_provide = arguments.keys() - kwargs_to_provide.keys()
    if cant_provide:
        raise Exception("Can't provide arguments: %s" % cant_provide)


``andi`` support typing.Union. If an argument is annotated
as ``Union[Foo, Bar]``, it means "both Foo and Bar objects are fine,
but callable prefers Foo":

.. code-block:: python

    def callback4(x: Union[Baz, Bar, Foo]):
        pass

    # Bar is preferred to Foo, and Baz is not available, so my_framework passes
    # Bar instance to ``x`` argument (``x = fetch_bar()``)
    my_framework(callback4)

``andi`` also supports typing.Optional types. If an argument is annotated
as optional, it means ``Union[<other types>, None]``. So usually framework
specifies that None is OK, and provides it; None has the least priority:

.. code-block:: python

    def callback4(foo: Optional[Foo], baz: Optional[Baz]):
        pass

    # foo=Foo(), baz=None is passed, because my_framework
    # supports Foo, but not Baz
    my_framework(callback4)

``andi`` only checks type-annotated arguments; arguments without annotations
are ignored.

Constructor Dependency Injection
--------------------------------

It is common for frameworks to ask users to define classes with a certain
interface, not just callbacks. ``andi`` can be used like this:

.. code-block:: python

    class UserClass:
        def __init__(self, foo: Foo):
            self.foo = foo
        # ...

    class MyFramework:
        # ...
        def create_instance(self, user_cls):
            kwargs_to_provide = andi.to_provide(user_cls.__init__,
                                                can_provide={Foo, Bar})
            # ... fill kwargs, based on ``kwargs_to_provide``
            return user_cls(**kwargs)

    obj = framework.create_instance(UserClass)

Pattern is the following:

1) ask user classes to declare all dependencies in ``__init__`` method,
2) then framework creates instances of these classes, passing all the
   required dependencies.

Instead of ``__init__`` you can also use a classmethod.

Recursive dependencies
----------------------

``andi`` can be used on different levels in a framework. For example,
framework supports callbacks which receive instances of
some BaseClass subclasses:

.. code-block:: python

    class UserClass(framework.BaseClass):
        def __init__(self, foo: Foo):
            self.foo = foo

    def callback(user: UserClass):
        # ...

    class MyFramework:
        # ...
        def create_instance(self, user_cls):
            kwargs_to_provide = andi.to_provide(user_cls.__init__,
                                                can_provide={Foo, Bar})
            # ... fill kwargs, based on ``kwargs_to_provide``, i.e.
            # create Foo and Bar objects somehow
            return user_cls(**kwargs)

        def call_callback(self, callback):
            kwargs_to_provide = andi.to_provide(
                callback,
                can_provide=self.is_allowed_callback_argument
            )
            kwargs = {}
            for name, user_cls in kwargs_to_provide.items():
                kwargs[name] = self.create_instance(user_cls)
            return callback(**kwargs)

        def is_allowed_callback_argument(self, cls):
            return issubclass(cls, framework.BaseClass)

In this example callback needs a dependency (UserClass object), and UserClass
object on itself has a dependency (Foo). So ``andi`` is used to find out these
dependencies, and then framework creates Foo object first, then
UserClass object, and then finally calls the callback.

Implementation can be recursive as well, e.g. Foo may need some dependencies
as well.

Why type annotations?
---------------------

``andi`` uses type annotations to declare dependencies (inputs).
It has several advantages, and some limitations as well.

Advantages:

1. Built-in language feature.
2. You're not lying when specifying a type - these
   annotations still work as usual type annotations.
3. In many projects you'd annotate arguments anyways, so ``andi`` support
   is "for free".

Limitations:

1. Callable can't have two arguments of the same type.
2. This feature could possibly conflict with regular type annotation usages.

If your callable has two arguments of the same type, consider making them
different types. For example, a callable may receive url and html of
a web page:

.. code-block:: python

    def parse(html: str, url: str):
        # ...

To make it play well with ``andi``, you may define separate types for url
and for html:

.. code-block:: python

    class HTML(str):
        pass

    class URL(str):
        pass

    def parse(html: HTML, url: URL):
        # ...

This is more boilerplate though.

You can also refactor ``parse`` to have a single argument:

.. code-block:: python

    @dataclass
    class Response:
        url: str
        html: str

    def parse(response: Response):
        # ...

Why doesn't andi handle creation of objects?
--------------------------------------------

Currently ``andi`` just inspects callable and chooses best concrete types
a framework needs to create and pass to a callable, without prescribing how
to create them. This makes ``andi`` useful in various contexts - e.g.

* creation of some objects may require asynchronous funnctions, and it
  may depend on libraries used (asyncio, twisted, etc.)
* in streaming architectures (e.g. based on Kafka) inspection may happen
  on one machine, while creation of objects may happen on different nodes
  in a distributed system, and then actually running a callable may happen on
  yet another machine.

It is hard to design API with enough flexibility for all such use cases.
That said, ``andi`` may provide more helpers in future,
once patterns emerge, even if they're useful only in certain contexts.

Contributing
============

* Source code: https://github.com/scrapinghub/andi
* Issue tracker: https://github.com/scrapinghub/andi/issues

Use tox_ to run tests with different Python versions::

    tox

The command above also runs type checks; we use mypy.

.. _tox: https://tox.readthedocs.io
