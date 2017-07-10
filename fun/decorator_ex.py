#!/usr/bin/python

def verbose(func):
    def wrapper():
        print 'Before execution: %s' % func.__name__
        func()
        print 'After execution: %s' % func.__name__
    return wrapper

@verbose
def greeting():
    print 'Hello, world!'

greeting()