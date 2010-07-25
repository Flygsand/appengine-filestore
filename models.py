from google.appengine.ext import db

class File(db.Model):
    name = db.StringProperty(required=True)
    content_type = db.StringProperty(default='application/octet-stream')
    last_modified = db.DateTimeProperty(auto_now=True)

class Fragment(db.Model):
    file = db.ReferenceProperty(File, collection_name='fragments', required=True)
    data = db.BlobProperty(required=True)
    
class Client(db.Model):
    nonce = db.IntegerProperty(default=0)

    def new_nonce(self):
        self.nonce += 1
        
