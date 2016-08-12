#!/usr/bin/env python 

import urllib2
import os
import sys
import re
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

monikers = {'windies'       : 'west indies',
            'men in blue'   : 'india',
            'proteas'       : 'south africa',
            'aussies'       : 'australia',
            'english'       : 'england',
            'baggy greens'  : 'australia',
            'black caps'    : 'new zealand',
            }

cric_url = 'http://www.espncricinfo.com/ci/engine/match/index.html'
cric_nations = 'http://www.espncricinfo.com/ci/content/site/cricket_squads_teams/index.html'
# List of cricket playing nations
espn_list = []

def search_in_a_tag(href):
    """
    param: the href attribute value and not the attribute itself
    return: True if the pattern is found in the href value
            False if the pattern is not found in the href value
    """
    return href and re.compile("/content/team/.*\.html").search(href)

def cricnation(country):
    """ 
    Does this country play cricket at all?
    param: country to be searched
    return: True cricket playing nation
            False non cricket playing nation
    """
    urlobj = urllib2.urlopen(cric_nations)
    
    if urlobj.getcode() != 200:
        print "Error in verifying the country! Please try again later."
        sys.exit(1)
    plain_html = urlobj.read()
    soap = bs(plain_html, "html.parser")
    
    # Incredible feature of find_all
    # find the country from ESPN or from the list of monikers
    for country_list in soap.find_all(href=search_in_a_tag):
        espn_nation = country_list.string.lower()
        in_nation = country.lower()
        if in_nation == espn_nation:
            return True
        elif in_nation in monikers:
            return True
        espn_list.append(espn_nation)
        
    return False

def compute():
    if sys.argv[1]:
        search_param = sys.argv[1]
        if not cricnation(search_param):
            print "You've asked for a nation that hasn't learnt to play this "\
                  "wonderful game yet. You should be interested in these "\
                  "countries instead."
            print '\n'.join(espn_list)
            sys.exit(1)
        
    #urlobj = urllib2.urlopen(cric_url)
    #if urlobj.getcode() != 200:
    #   print "Unable to get the scores now. Please try again later!"
    #    sys.exit(1)

    #plain_html = urlobj.read()
    #soup = bs(plain_html, "html.parser")

if __name__ == "__main__":
    compute()
