Process Timer
=================

Installation
------------

From source code:

`python setup.py install`

From pypi:

`pip install process-timer`

Usage
-----

```py
    import time
    from process_timer import timeout

    @timeout(5)
    def mytest():
        print("Start")
        for i in range(1,10):
            time.sleep(1)
            print(f"{i} seconds have passed")

    if __name__ == '__main__':
        mytest()
```

Specify an alternate exception to raise on timeout:

```py
    import time
    from process_timer import timeout

    @timeout(5, timeout_exception=StopIteration)
    def mytest():
        print("Start")
        for i in range(1,10):
            time.sleep(1)
            print(f"{i} seconds have passed")

    if __name__ == '__main__':
        mytest()
```

Multithreading
--------------

By default, timeout-decorator uses signals to limit the execution time
of the given function. This appoach does not work if your function is
executed not in a main thread (for example if it's a worker thread of
the web application). There is alternative timeout strategy for this
case - by using multiprocessing. To use it, just pass
``use_signals=False`` to the timeout decorator function:

```py
    import time
    from process_timer import timeout

    @timeout(5, use_signals=False)
    def mytest():
        print("Start")
        for i in range(1,10):
            time.sleep(1)
            print(f"{i} seconds have passed")

    if __name__ == '__main__':
        mytest()
```

>_**Warning**_
    Make sure that in case of multiprocessing strategy for timeout, your function does not return objects which cannot
    be pickled, otherwise it will fail at marshalling it between master and child processes.

Acknowledgement
---------------

<ul>Timeout Decorator - https://github.com/pnpnpn/timeout-decorator</ul>
<ul>http://www.saltycrane.com/blog/2010/04/using-python-timeout-decorator-uploading-s3/</ul>
<ul>https://code.google.com/p/verse-quiz/source/browse/trunk/timeout.py</ul>

Contribute
----------

I would love for you to fork and send me pull request for this project.
Please contribute.

License
-------

This software is licensed under the [MIT license](http://en.wikipedia.org/wiki/MIT_License)

See [License file](https://github.com/sprajosh/process-timer/blob/master/LICENSE.txt)
