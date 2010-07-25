import config
import hmac, hashlib
from datetime import datetime, timedelta
from models import Client

def verify(request):
    client_id = request.headers.get('X-AEFS-ClientId', None)
    signature = request.headers.get('X-AEFS-Signature', None)
    body = request.body
    
    if client_id and signature:
        client = Client.get_by_key_name(client_id)
        if not client:
            client = Client(key_name=client_id)
            
        h = hmac.new(config.shared_secret, client_id + str(client.nonce) + body, hashlib.sha1)
        client.new_nonce()
        client.put()
        return h.hexdigest() == signature
    else:
        return False

def authenticated(fn):
    def wrapper(handler, *args, **kwargs):

        if verify(handler.request):
            fn(handler, *args, **kwargs)
        else:
            handler.error(401)

    return wrapper
            
