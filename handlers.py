import config
import urllib
from google.appengine.ext import webapp
from uuid import uuid4
from models import File, Fragment
from utils import chunks

class FileHandler(webapp.RequestHandler):
    def get(self, file_uuid):
        file = File.get_by_key_name(file_uuid)

        if file:
            self.response.headers.add_header('Content-Disposition', 'inline', filename=file.name)
            self.response.headers.add_header('Content-Type', file.content_type)

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
