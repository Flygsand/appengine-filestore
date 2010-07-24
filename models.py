from google.appengine.ext import db

class File(db.Model):
    name = db.StringProperty(required=True)
    content_type = db.StringProperty(default='application/octet-stream')         

class Fragment(db.Model):
    file = db.ReferenceProperty(File, collection_name='fragments')
    data = db.BlobProperty(required=True)
    
