# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file LICENSE, which
# you should have received as part of this distribution.
#

# flake8: noqa

from aiohttp.hdrs import *
from multidict import istr

#: Defines CouchDB Proxy Auth username
X_AUTH_COUCHDB_USERNAME = istr('X-Auth-CouchDB-UserName')
#: Defines CouchDB Proxy Auth list of roles separated by a comma
X_AUTH_COUCHDB_ROLES = istr('X-Auth-CouchDB-Roles')
#: Defines CouchDB Proxy Auth token
X_AUTH_COUCHDB_TOKEN = istr('X-Auth-CouchDB-Token')
