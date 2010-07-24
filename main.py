#!/usr/bin/env python

import urllib
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from handlers import FileHandler

import datastore_cache
datastore_cache.DatastoreCachingShim.Install()

if __name__ == '__main__':
    application = webapp.WSGIApplication([('/([^/]+)', FileHandler)], debug=True)
    util.run_wsgi_app(application)
