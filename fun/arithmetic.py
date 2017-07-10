#!/usr/bin/python


def operation(msg):
    def decorator(func):
        def wrapper():
            print 'Performing ' + msg
            func()
        return wrapper
    return decorator


@operation('addition')
def addition():
    print 3 + 4


@operation('multiplication')
def multi():
    print 3 * 4


@operation('subtraction')
def subt():
    print 3 - 4


@operation('division')
def div():
    print 3 / 4


addition()
multi()
subt()
div()