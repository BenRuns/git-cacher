#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import datetime

from google.appengine.api import urlfetch
from google.appengine.api import memcache

class MainHandler(webapp2.RequestHandler):

    def get(self):
    	github = self.request.get('github')
    	repo = self.request.get('repo')
    	item = memcache.get( github + 'randomhash' + repo)

    	if not item and github and repo  or (datetime.datetime.now() - item[1]) > datetime.timedelta(hours = 3) :

    		url = 'https://api.github.com/repos/' + github + '/' +repo
    		result = urlfetch.fetch(url)
    		item = [ result.content,  datetime.datetime.now() ]
    		memcache.set(key = github + 'randomhash' + repo, value= item ) 
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
    	
        self.response.write(item[0])

class UserHandler(webapp2.RequestHandler):

    def get(self):
        author = self.request.get('author')
        
        item = memcache.get( author )

        if not item and author or (datetime.datetime.now() - item[1]) > datetime.timedelta(hours = 3) :

            url = 'https://api.github.com/users/' + author 
            result = urlfetch.fetch(url)
            item = [ result.content,  datetime.datetime.now() ]
            memcache.set(key = author, value= item ) 
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        
        self.response.write(item[0])

class StatsHandler(webapp2.RequestHandler):

    def get(self):
        github = self.request.get('github')
        repo = self.request.get('repo')
        item = memcache.get( github + 'stats' + repo)

        if not item and github and repo or (datetime.datetime.now() - item[1]) > datetime.timedelta(hours = 3) :

            url = 'https://api.github.com/repos/' + github + '/' + repo + "/stats/contributors"
            result = urlfetch.fetch(url)
            item = [ result.content,  datetime.datetime.now() ]
            memcache.set(key = github + 'stats' + repo, value= item ) 
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        
        self.response.write(item[0])



app = webapp2.WSGIApplication([
    ('/stats/contributors', StatsHandler),
    ('/users', UserHandler),
    ('/', MainHandler)
], debug=True)
     
