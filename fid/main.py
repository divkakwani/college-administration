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
import cgi
import urllib
import os

import myhashlib
import webapp2

from boilerplate import *
from profile import *
from user_accounts import *


class MainHandler(Handler):
    
    def get(self):
        username = str(self.request.cookies.get('username'))
        # Send if username is valid
        error = str(self.request.get('error'))
        self.render_page('templates/front.html', {'username': myhashlib.check_secure_val(username), 'error': error})
        

app = webapp2.WSGIApplication([('/', MainHandler), ('/profile', ProfileViewer), ('/profile/edit', EditProfile),('/signup', SignUp), ('/pic', GetPic), ('/autocomplete', AutoComplete), ('/login', Login), ('/logout', LogoutHandler)
], debug=True)
