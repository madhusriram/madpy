#!/usr/bin/env python

# Problem: https://changelog.com/can-your-favorite-programming-language-score-a-goal/
# In case the link expires below is a short description
# g()('al') is a challenge whereby you need to write in as many languages as 
# possible code which enables the code g()('al') to return the string "goal", the 
# code g()()('al') to return the string "gooal", the code g()()()('al') return 
# the string "goooal", etc.


def g(al=None, count=0):
    if al:
        return 'g' + (count * 'o') + al
    else:
        return lambda al=None: g(al,count+1)

print "Testing: "
print "g('al'): %s" %g('al')
print "g()('al'): %s" %g()('al')
print "g()()('al'): %s" %g()()('al')
print "g()()()('al'): %s" %g()()()('al')
print "g()()()()('al'): %s" %g()()()()('al')
