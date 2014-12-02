
import webapp2
import myhashlib
import util

from boilerplate import *

from google.appengine.ext import ndb
from google.appengine.api import memcache


class Profile(ndb.Model):
    # Models a profile entry 
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    photo = ndb.BlobProperty()
    # qualifications = 
    email = ndb.StringProperty()
    # achievements = ndb.StringListProperty()
    # phone = ndb.
    # publications = ndb.StringListProperty()
    age = ndb.IntegerProperty()
    # dob = ndb.DateTimeProperty()


class ProfileViewer(Handler):
    def get(self):
        logged_user = str(self.request.cookies.get('username'))
        username = self.request.get('username')
        profile = memcache.get(username)
        if not profile:
            profile = Profile.query(Profile.id == username).get()
            if profile:
                self.render_page('templates/profile.html', {'profile': profile, 'username': myhashlib.check_secure_val(logged_user)})
                memcache.set(username, profile)
            else:
                self.redirect('/?error=Not+Found')
        else:
            self.render_page('templates/profile.html', {'profile': profile, 'username': myhashlib.check_secure_val(logged_user)})
        


class GetPic(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'image/jpeg'
        username = self.request.get('username')
        profile = memcache.get(username) 
        if not profile:
            profile = Profile.query(Profile.id == username ).get()
            memcache.set(username, profile)
        self.response.out.write(profile.photo)

class EditProfile(Handler):
    
    def get(self):
        cookie_val = str(self.request.cookies.get('username'))
        try:
            username = myhashlib.check_secure_val(cookie_val)
            profile = memcache.get(username)
            if not username:
                self.redirect("/login")
            else:
                self.render_page('templates/editprofile.html', {'username': username, 'profile': profile})
        except:
            self.redirect("/login")

    def post(self):
        username = myhashlib.check_secure_val(str(self.request.cookies.get('username')))
        profile = Profile(id = username, name = self.request.get('name'), email = self.request.get('email'),
                          age = util.parseInt(self.request.get('age')), photo = self.request.get('photo'))
        profile.put()
        self.redirect('/')

   