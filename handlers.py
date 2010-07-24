import config
import urllib
from google.appengine.ext import webapp
from time import time
from uuid import uuid4
from models import File, Fragment
from utils import chunks, http_format_date, http_parse_date

class FileHandler(webapp.RequestHandler):
    def get(self, file_uuid):
        file = File.get_by_key_name(file_uuid)

        if file:
            self.response.headers['Last-Modified'] = http_format_date(file.last_modified)
            self.response.headers['Cache-Control'] = 'max-age=%d' % config.cache_expiry

            if_modified_since = http_parse_date(self.request.headers.get('If-Modified-Since', None))
            if if_modified_since and if_modified_since >= file.last_modified.replace(microsecond=0):
                self.response.set_status(304)
            else:
                self.response.headers['Content-Disposition'] = 'inline; filename=%s' % file.name
                self.response.headers['Content-Type'] = file.content_type
                self.response.headers['Expires'] = http_format_date(time() + config.cache_expiry)

                for fragment in file.fragments:
                    self.response.out.write(fragment.data)
        else:
            self.error(404)

    def put(self, filename):
        file_uuid = uuid4().hex
        
        file = File(name=str(urllib.unquote(filename)),
             content_type=self.request.headers.get('Content-Type', None),
             key_name=file_uuid)
        file.put()

        for chunk in chunks(self.request.body, config.max_fragment_size):
            Fragment(file=file, data=chunk).put()

        self.response.set_status(201)
        self.response.out.write(file_uuid)

    def delete(self, file_uuid):
        file = File.get_by_key_name(file_uuid)
        
        if file:
            map(lambda f: f.delete(), file.fragments)
            file.delete()
        else:
            self.error(404)
