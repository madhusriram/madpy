#!/usr/bin/env python 

import urllib2
import os
import sys
import string
import re
from bs4 import BeautifulSoup as bs
from prettytable import PrettyTable

monikers = {'windies'       : 'West Indies',
            'men in blue'   : 'India',
            'proteas'       : 'South Africa',
            'aussies'       : 'Australia',
            'english'       : 'England',
            'baggy greens'  : 'Australia',
            'black caps'    : 'New Zealand',
            }

cric_url = 'http://www.espncricinfo.com/ci/engine/match/index.html?view=live'
cric_nations = 'http://www.espncricinfo.com/ci/content/site/cricket_squads_teams/index.html'
# List of cricket playing nations
espn_list = []
# Input formatted search team
search_team = ""
search_team_match = 0

def search_in_a_tag(href):
    """
    param: the href attribute value and not the attribute itself
    return: True if the pattern is found in the href value
            False if the pattern is not found in the href value
    """
    return href and re.compile("/content/team/.*\.html").search(href)

def get_url(url):
	""" """
	urlobj = urllib2.urlopen(url)

	if urlobj.getcode() != 200:
		print "Error in connecting to the database! Please try again later."
		sys.exit(1)
	plain_html = urlobj.read()
	soap = bs(plain_html, "html.parser")

	return soap

def cricnation(country):
    """ 
    Does this country play cricket at all?
    param: country to be searched
    return: True cricket playing nation
            False non cricket playing nation
    """
    soap = get_url(cric_nations)
    global search_team

    # Incredible feature of find_all
    # find the country from ESPN or from the list of monikers
    for country_list in soap.find_all(href=search_in_a_tag):
        espn_nation = country_list.string.lower()
        in_nation = country.lower()
        if in_nation in monikers:
            search_team = monikers.get(in_nation)
            return True
        if in_nation == espn_nation:
            search_team = country_list.string	
            return True
        espn_list.append(country_list.string)
        
    return False

def test_or_oneday(date):
	""" 
	:param date duration of the match
	Aug 11-15, 2016 - Test match
	Aug 13, 2016 - One day
	:return Test if a 3-day or a 5-day test match
			One day if a 1-day event
	"""
	if re.compile("^\w{3}\s\d{1,2}\-\d{1,2}\,\s\d{1,4}$").search(date):
		return "Test"
	elif re.compile("^\w{3}\s\d{1,2}\,\s\d{1,4}$").search(date):
		return "One day" # Can be a T-20 as well	

def check_score(scores):
	"""
	:param scores innings scores of a team
	
	Notes: 328 & 88/4 (31 ov) or 542 or ""
	"""
	
	if len(scores) == 1:
		# 1st innings played
		scores.append("DNB")
	elif len(scores) < 1:
		# Both the innings not started
		scores.append("DNB")
		scores.append("DNB")

	return scores

def scoreboard(inn_1, inn_2, date, match_status, venue, match_type):
	""" 
	:param search_team team of interest, default None
	:param inn_1 1st team's score
	:param inn_2 2nd teams's score
	:param date duration of the match
	:param match_status status of the match
	:param venue where are they playing?
	:param match_type test or one day
	"""
	# Test match template
	testtable = PrettyTable(["Country","Innings-1","Innings-2"])
	oditable  = PrettyTable(["Country","Innings"])
	
	team_a_score = re.split(' {3,}',inn_1)
	team_b_score = re.split(' {3,}',inn_2)
	
	if search_team:
		if (search_team in team_a_score[0] or search_team in team_b_score[0]):
			global search_team_match
			search_team_match = 1
			pass	
		else:
			return
	else:		# This is the default case, no filter criterion
		pass

	if match_type == "Test":
		a_score = check_score(re.split(' &', team_a_score[1]))
		b_score = check_score(re.split(' &', team_b_score[1]))
		# template: team, innings-1 score, innings-2 score
		testtable.add_row([team_a_score[0], a_score[0], a_score[1]])
		testtable.add_row([team_b_score[0], b_score[0], b_score[1]])
		print testtable
	elif match_type == "One day":
		oditable.add_row([team_a_score[0], team_a_score[1]])
		oditable.add_row([team_b_score[0], team_b_score[1]])
		print oditable

def parse_and_print():
	""" """
	soap = get_url(cric_url)
	
	for live_match in soap.find_all('section', attrs={'data-matchstatus':'current'}):
		venue = live_match.find('a').string
		date = live_match.find('span',attrs={'class':'bold'}).text
		inn_1 = live_match.find('div',attrs={'class':'innings-info-1'}).text
		inn_2 = live_match.find('div',attrs={'class':'innings-info-2'}).text
		match_status = live_match.find('div',attrs={'class':'match-status'}).text
		
		scoreboard(inn_1, inn_2, date, match_status, venue, test_or_oneday(date))

def compute():
	"""
	:param search_param user interested country or it's moniker
	
	"""
	search_param = ""
	if len(sys.argv) > 1:
		search_param = sys.argv[1]
		if not cricnation(search_param):
			print "You've asked for a nation that hasn't learnt to play this "\
                  "wonderful game yet. Instead you should be interested in these "\
				  "countries:"
			for index, country in enumerate(espn_list, start = 1):
				print "%d: " % index + country
			sys.exit(1)

	# Get live matches
	parse_and_print()	
	if search_param and not search_team_match:
		print "++++++++++++++++++++++++++++++++++++"
		print "No live matches for %s yet" % search_team
		print "++++++++++++++++++++++++++++++++++++"

if __name__ == "__main__":
    compute()


# To do:
# Usage printing

