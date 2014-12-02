import webapp2
import myhashlib
from boilerplate import *
from google.appengine.ext import ndb
import trie
import util
import json

class User(ndb.Model):
    # User's login details 
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    password = ndb.StringProperty()

class Login(Handler):
    
    def get(self):
        username = myhashlib.check_secure_val(str(self.request.cookies.get('username')))
        if username:
            # Already logged in
            self.redirect('/')
        else:
            self.render_page("templates/login.html", {'error': ''})
        
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        # query the database
        query = ndb.gql("SELECT * FROM User WHERE username = :1 ", username )
        user = query.get()
        if user:
            # validate password
            if myhashlib.check_hash_pass(password, user.password):
                self.response.headers.add_header('Set-Cookie', 'username=%s' % str(myhashlib.make_secure_val(user.username)))
                self.redirect('/')
            else:
                self.render_page("templates/login.html", {'error': 'Password Invalid'})
        else:
            self.render_page("templates/login.html", {'error': 'Username does not exist'})
        
        
    
class SignUp(Handler):
    
    def get(self):
        self.render_page('templates/signup.html', {})
    
    def post(self):
        username = self.request.get('username')
        name = self.request.get('name')
        password = self.request.get('password')
        hashed_pass = myhashlib.hash_pass(password)
        new_user = User(username = username, name = name, password = hashed_pass)
        new_user.put()
        global names_trie
        if names_trie:
            names_trie.addWord(new_user.name.lower(), new_user.username)
        self.response.headers.add_header('Set-Cookie' , 'username=%s' % str(myhashlib.make_secure_val(username)))
        self.redirect('/profile/edit')

 
class LogoutHandler(Handler):
    
    def get(self):
        self.response.headers.add_header('Set-Cookie' , 'username=; Path=/'  )
        self.redirect('/')
        
        
class AutoComplete(Handler):
    def get(self):
        global names_trie
        if not names_trie:
            # Add later : Pickle the trie
            names_trie = trie.Trie()
            users = ndb.gql("SELECT * FROM User")
            for user in users:
                names_trie.addWord(user.name.lower(), user.username)
        all_names = names_trie.wordsStartingFrom(self.request.get('q').lower())
        result = []
        for name in all_names:
            result.append((util.capitalize_name(name[0]), name[1]))
        jsonStr = json.dumps(result)
        self.response.headers['Content-Type'] = 'application/json; charset=iso-8859-1'
        self.response.write(jsonStr)
            
