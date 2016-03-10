from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_auth,logout
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re
import urllib2
from fuzzywuzzy import process
import socket
import json
from datetime import datetime, timedelta,date
from aue.models import Enquiry
from fuzzywuzzy import fuzz
import logging
logger = logging.getLogger(__name__)

def index(request):
    """
    Automated Usability Evaluation index page
    """
    #Total number of record to be display in search result
    no_record_count = [1,2,3,4]
    return render(request, 'aue/index.html', {"no_record_count":no_record_count})


def get_link(input_url=None):
    """
    To get inner link of given link
    """
    return_list = []
    try:
        http = httplib2.Http()
        status, response = http.request(input_url)
    except:
        response = []
        logger.exception("%s is not a valid URL."%(input_url))
        

    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        #Filter only link from web page(Given search url)
        if link.has_key('href'):
            url = link['href'] 
            try:
                if re.match('^http', url):
                    url = url 
                else:
                    #In relative url add base url
                    url = "".join([input_url,url])
                return_list.append(url)
            except:
                logger.exception("%s URL  cananot be open."%(url))
    return_list = set(return_list)
    return list(return_list)

def get_filter_link(link_choice,goal=None,min_score=None,max_limit=4,type=0):
    """
    To get relevent link from list of link
    """
    if min_score:
        min_score = int(min_score)
    else:
        min_score = 60
    scored_link_list = []
    scored_link_list_raw = process.extract(goal,link_choice,limit=max_limit)
    logger.info("Score details for goal {0} with statistics {1}. minimum score {2}".format(goal,scored_link_list_raw,min_score))
    try:
        if scored_link_list_raw:
            for i in list(scored_link_list_raw):
                link = i[0]
                if int(type) != 1:
                    score = i[1]
                    if int(score) >= min_score:
                        scored_link_list.append(link)
                    logger.info("PARTIAL MATCH : Final score is {0} of url {1}  for goal {2}".format(score,link,goal))
                else:
                    score = fuzz.token_set_ratio(goal,link)
                    logger.info("EXACT MATCH : Final score is {0} of url {1}  for goal {2}".format(score,link,goal))
                    if int(score) >= min_score:
                        scored_link_list.append(link)
    except:
        logger.exception("Error occure in get_filter_link() function")
    return scored_link_list


def get_search_result(request):
    """
    Function to get best possible url 
    """
    
    type = request.POST.get("type",0)
    min_score = request.POST.get("min_score",60)
    input_url = request.POST.get("input_url","")
    #remove end slash for use search url as base url
    input_url = input_url.rstrip("/")
    input_goal = request.POST.get("input_goal","")
    #to get IP address of system
    try:
    	ip_address = socket.gethostbyname(socket.gethostname())
    except:
    	ip_address = ""
        logger.exception("Error in get system ip address")
    if input_url and input_goal:
    	try:
    		Enquiry.objects.create(ip_address=ip_address,url=input_url,goal=input_goal)    	
    	except:
            logger.exception("Error in insert enquiry data")
    #logger
    logger.info("IP address {0} has searched URL {1} with GOAL {2}".format(ip_address,input_url,input_goal))
    link_list = get_link(input_url)
    final_scored_link_list = get_filter_link(link_list,input_goal,min_score,4,type)
    
    return_object = {"search_result":final_scored_link_list}
    return HttpResponse(json.dumps(return_object),
            content_type="application/json")
