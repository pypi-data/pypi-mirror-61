pyeventbus3
=========================

.. image:: https://travis-ci.org/n89nanda/pyeventbus.svg?branch=master
    :target: https://travis-ci.org/n89nanda/pyeventbus
    
pyeventbus3 is a publish/subscribe event bus for Python 3. (Fork of pyeventbus for python 2.7)

+ simplifies the communication between python classes 
+ decouples event senders and receivers
+ performs well threads, greenlets, queues and concurrent processes
+ avoids complex and error-prone dependencies and life cycle issues
+ makes code simpler
+ has advanced features like delivery threads, workers and spawning different processes, etc.
+ is tiny (3KB archive) 

pyeventbus3 in 3 steps:

1. Define events::
        
            class MessageEvent:
                # Additional fields and methods if needed
                def __init__(self):
                    pass
                 
2. Prepare subscribers: Declare and annotate your subscribing method, optionally specify a thread mode::

            from pyeventbus3.pyeventbus3 import *
            
            @subscribe(onEvent=MessageEvent)
            def func(self, event):
                # Do something
                pass
                
   
   Register your subscriber. For example, if you want to register a class in Python::
            
            from pyeventbus3.pyeventbus3 import *
            
            class MyClass:
                def __init__(self):
                    pass
                
                def register(self, myclass):
                    PyBus.Instance().register(myclass, self.__class__.__name__)
                    
            # then during initilization
            
            myclass = MyClass()
            myclass.register(myclass)
            
3. Post events::
        
            from pyeventbus3.pyeventbus3 import *
            
            class MyClass:
                def __init__(self):
                    pass
                
                def register(self, myclass):
                    PyBus.Instance().register(myclass, self.__class__.__name__)
                    
                def postingAnEvent(self):
                    PyBus.Instance().post(MessageEvent())
              
             myclass = MyClass()
             myclass.register(myclass)
             myclass.postingAnEvent()
            

Modes: pyeventbus can run the subscribing methods in 5 different modes

1. POSTING::

    Runs the method in the same thread as posted. For example, if an event is posted from main thread, the subscribing method also runs in the main thread. If an event is posted in a seperate thread, the subscribing method runs in the same seperate method
    
    This is the default mode, if no mode has been provided::
        
    @subscribe(threadMode = Mode.POSTING, onEvent=MessageEvent)
    def func(self, event):
        # Do something
        pass
    
2. PARALLEL::
    
    Runs the method in a seperate python thread::
        
    @subscribe(threadMode = Mode.PARALLEL, onEvent=MessageEvent)
    def func(self, event):
        # Do something
        pass
        
3. GREENLET::

    Runs the method in a greenlet using gevent library::
            
    @subscribe(threadMode = Mode.GREENLET, onEvent=MessageEvent)
    def func(self, event):
        # Do something
        pass
    
4. BACKGROUND::
    
    Adds the subscribing methods to a queue which is executed by workers::
            
    @subscribe(threadMode = Mode.BACKGROUND, onEvent=MessageEvent)
    def func(self, event):
        # Do something
        pass

    There is 10 workers by default, see exemple to modify this number.

3. CONCURRENT::

    Runs the method in a seperate python process::
            
    @subscribe(threadMode = Mode.CONCURRENT, onEvent=MessageEvent)
    def func(self, event):
        # Do something
        pass
   
   
 
Adding pyeventbus to your project::

    pip install pyeventbus3

 
Example::
    
    git clone https://github.com/FlavienVernier/pyeventbus.git
    
    cd pyeventbus
    
    virtualenv venv
    
    source venv/bin/activate
    
    pip install pyeventbus
    
    python example.py
    

Benchmarks and Performance::
        
        
        Refer /pyeventbus/tests/benchmarks.txt for performance benchmarks on CPU, I/O and networks heavy tasks.
        
        Run /pyeventbus/tests/test.sh to generate the same benchmarks.
        
        Performance comparison between all the modes with Python and Cython
        
.. image:: pyeventbus/tests/Benchmarks.png
            :width: 2000px
            :align: center
            :height: 1000px
            :alt: alternate text

Inspiration

        Inspired by Eventbus from greenrobot: https://github.com/greenrobot/EventBus
