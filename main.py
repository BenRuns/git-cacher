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

class GitHandler(webapp2.RequestHandler):

    def get(self,thing):
    	item = memcache.get( thing )
    	if not item or (datetime.datetime.now() - item[1]) > datetime.timedelta(hours = 3):
            url = 'https://api.github.com/' + thing
            try: 
              result = urlfetch.fetch(url)
              item = [ result.content,  datetime.datetime.now() ]
            except:
              item = [json.dumps({'message': "Request to github failed - try again later. Something might be wrong with github's site. Check with github " }), datetime.datetime.now() ]
            memcache.set(key =  thing, value= item )   
            
        self.response.headers['Content-Type'] = 'application/json'   
        self.response.headers.add_header("Access-Control-Allow-Origin", "*")
        self.response.write(item[0])

class FlushHandler(webapp2.RequestHandler):

     def get(self):
        
        memcache.flush_all()

        self.response.write("flushed cache")

class MainHandler(webapp2.RequestHandler):

    def get(self):

        self.response.write("""
            <html>
            <head>
            <title>Github Cacher</title>
            </head>
            <body>

            <p>Hello! 
            This is a little app that I'm using to cache requests to Github's api 
            so that I don't hit their limit on requests quite as fast. Please don't abuse this service.
            </p>
            <p> Code is at <a href="https://github.com/BenRuns/git-cacher">Github</a>
            </p>
            <p>
            to use this, just replace api.github.com with
            git-hub-cacher.appspot.com</p>
            <p> to flush the cache on this site,
            visit git-hub-cacher.appspot.com/admin/flush </p>
            <p> This will make me hit github's rate limits sooner so please avoid flushing the cache automatically ...etc..</p>


            </body>
            </html>
            </html>


            """)

        




app = webapp2.WSGIApplication([
    ('/admin/flush', FlushHandler),
    ('/(.+)', GitHandler),
    ('/', MainHandler)
   
], debug=True)
     
