
import hashlib
import hmac
import random
import string


def rand_salt():
    return "".join( random.choice(string.letters) for x in range(5) )   # generate a random 5-letter string
    
def make_secure_val(username , salt = None ):
    if not salt:
        salt = rand_salt()
    h = hmac.new(salt, username).hexdigest()
    return '%s|%s|%s' % (username, h, salt)
    
def check_secure_val(h):
    try:
        username = h.split('|')[0]
        if make_secure_val(username, h.split('|')[2]) == h:
            return username
    except:
        pass
        
def hash_pass(password, salt = None):
    if not salt:
        salt = rand_salt()
    h = hashlib.sha256(salt + password).hexdigest()
    return '%s,%s' % (h, salt)
    
def check_hash_pass(password , hashPass):
    try:
        salt = hashPass.split(',')[1]
        if salt:
            return hash_pass(password , salt) == hashPass
    except:
        pass
